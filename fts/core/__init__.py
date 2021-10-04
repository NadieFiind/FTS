from fts.utils import stringToDict
from fts.core.exceptions import InvalidSyntax
from typing import Any, List, Dict, Tuple, Optional


class Task:
	
	def __init__(
		self, content: str, *,
		fts: "FTS", parent: Optional["Task"] = None,
		priority: int = 0, scheduler: Optional["Scheduler"] = None,
		line_num: int
	):
		self.fts = fts
		self.parent = parent
		self._content = content
		self.priority = priority
		self.scheduler = scheduler
		self.subtasks: List[Task] = []
		self.line_num = line_num  # Line number of this task in the FTS format file.
	
	@property
	def content(self) -> str:
		return self._content
	
	@content.setter
	def content(self, value: str) -> None:
		self._content = value
		self.fts._update_task(self)
	
	@property
	def id(self) -> str:
		if self.parent:
			return str(self.parent.id) + str(self.parent.subtasks.index(self))
		
		return str(self.fts.tasks.index(self))
	
	def call_scheduler(self) -> Tuple[Optional[bool], str]:
		if self.scheduler is None:
			if self.parent and self.parent.scheduler:
				return self.parent.scheduler.call(self)
			
			return None, "No Schedule"
		
		return self.scheduler.call(self)


class FTS:
	
	def __init__(self, fts_format: str, *, indent_char: str = "	"):
		self._parser = FTSFParser(fts_format, indent_char=indent_char)
		self._editor = FTSFEditor(fts_format, indent_char=indent_char)
		self.tasks: List[Task] = self._parser.get_tasks(self)
	
	def _update_task(self, task: Task) -> None:
		self._editor.edit_task(task)
		self._parser.value = self._editor.value
	
	def add_task(
		self, content: str, *, parent: Optional[Task] = None,
		priority: int = 0, scheduler: Optional["Scheduler"] = None,
		position: int = 0
	) -> Task:
		task = Task(
			content,
			fts=self,
			parent=parent,
			priority=priority + parent.priority if parent else priority,
			scheduler=scheduler,
			line_num=-1
		)
		
		if parent:
			parent.subtasks.insert(position, task)
		else:
			self.tasks.insert(position, task)
		
		task.line_num = self._editor.insert_task(task)
		self._parser.value = self._editor.value
		
		self.tasks = self._parser.get_tasks(self)
		return task
	
	def to_string(self) -> str:
		return self._editor.value
	
	def delete_task_by_id(self, id: str) -> None:
		task = self.get_task_by_id(id)
		if task is None:
			return
		
		self._editor.remove_task(task)
		
		if task.parent:
			task.parent.subtasks.remove(task)
		else:
			task.fts.tasks.remove(task)
		
		self._parser.value = self._editor.value
		self.tasks = self._parser.get_tasks(self)
	
	def get_task_by_id(self, id: str) -> Optional[Task]:
		def get_subtask(task: Task, *, level: int = 1) -> Optional[Task]:
			for subtask in task.subtasks:
				if subtask.id == id:
					return subtask
				
				if subtask.id[level] == id[level]:
					return get_subtask(subtask, level=level + 1)
			
			return None
		
		for task in self.tasks:
			if task.id == id:
				return task
			
			if task.id == id[0]:
				return get_subtask(task)
		
		return None


class FTSFParser:
	
	def __init__(self, fts_format: str, *, indent_char: str = "	") -> None:
		self.value = fts_format
		self.indent_char = indent_char
	
	def get_tasks(self, fts: FTS) -> List[Task]:
		tasks: List[Task] = []
		
		for (line_num, line), hanging_lines in stringToDict(
			self.value, indent=self.indent_char
		).items():
			# Remove comments.
			line = line.split("~#")[0]
			
			# Ignore empty lines.
			if not line:
				continue
			
			def set_subtasks(task: Task, lines: Dict[str, Any]) -> None:
				subtasks: List[Task] = []
				
				for (line_num, line), hanging_lines in lines.items():
					# Remove comments.
					line = line.split("~#")[0]
					
					# Ignore empty lines.
					if not line:
						continue
					
					priority, scheduler = self._get_priority_and_scheduler(line)
					subtask = Task(
						self._get_content(line),
						fts=fts, parent=task,
						priority=priority + task.priority,
						scheduler=scheduler,
						line_num=int(line_num)
					)
					
					set_subtasks(subtask, hanging_lines)
					subtasks.append(subtask)
				
				task.subtasks = subtasks
			
			priority, scheduler = self._get_priority_and_scheduler(line)
			task = Task(
				self._get_content(line), fts=fts,
				priority=priority, scheduler=scheduler,
				line_num=int(line_num)
			)
			
			set_subtasks(task, hanging_lines)
			tasks.append(task)
		
		return tasks
	
	def _get_content(self, line: str) -> str:
		for index, char in enumerate(line):
			if char == ">":
				return line[index + 1:].strip()
		
		raise InvalidSyntax()
	
	def _get_priority_and_scheduler(
		self, line: str
	) -> Tuple[int, Optional["Scheduler"]]:
		cursor = 0
		
		def get_priority() -> int:
			nonlocal cursor
			
			for index, char in enumerate(line):
				cursor += 1
				
				if char.isspace():
					continue
				
				if char != "{":
					cursor = index
					return 0
				
				priority = ""
				
				for char in line[index + 1:]:
					cursor += 1
					
					if char == "}":
						break
					
					priority += char
				
				return int(priority or 0)
			
			raise InvalidSyntax()
		
		def get_scheduler() -> Optional[Scheduler]:
			scheduler_code = ""
			
			for index, char in enumerate(line[cursor:]):
				if char == ">":
					if scheduler_code.isspace() or scheduler_code == "":
						return None
					
					return Scheduler.from_code(scheduler_code.strip())
				
				scheduler_code += char
			
			raise InvalidSyntax()
		
		return get_priority(), get_scheduler()


class FTSFEditor:
	
	def __init__(self, fts_format: str, *, indent_char: str = "	") -> None:
		self.value = fts_format
		self.indent_char = indent_char
	
	def edit_task(self, task: Task) -> None:
		lines = self.value.splitlines()
		line = lines[task.line_num - 1]
		comment: Optional[str]
		
		if "~#" in line:
			non_comment, comment = line.split("~#")
		else:
			non_comment = line
			comment = None
		
		prefix, content = non_comment.split(">")
		new_line = f"> {task.content} {f'~#{comment}' if comment else ''}".strip()
		
		if task.scheduler is not None:
			new_line = f"{task.scheduler.code} " + new_line
		
		if task.priority != 0:
			new_line = f"{{{task.priority}}} " + new_line
		
		indent_level = len(task.id) - 1
		new_line = self.indent_char * indent_level + new_line
		
		new_value = lines[:task.line_num - 1] + [new_line] + lines[task.line_num:]
		self.value = "\n".join(new_value).strip() + "\n"
	
	def insert_task(self, task: Task) -> int:
		def flatten_subtasks(task: Task) -> List[Task]:
			result = []
			
			def loop(tasks: List[Task]) -> None:
				nonlocal result
				for task in tasks:
					result.append(task)
					loop(task.subtasks)
			
			loop(task.subtasks)
			return result
		
		prev_task: Optional[Task]
		
		if task.parent:
			task_index = task.parent.subtasks.index(task)
			
			if task_index == 0:
				prev_task = task.parent
			else:
				prev_task = task.parent.subtasks[task_index - 1]
		else:
			task_index = task.fts.tasks.index(task)
			
			if task_index == 0:
				prev_task = None
			else:
				prev_task = task.fts.tasks[task_index - 1]
		
		################################################
		#                                              #
		# FUCK THIS CODE! IDK WHAT'S GOING ON ANYMORE. #
		#                                              #
		################################################
		
		lines = self.value.splitlines()
		new_line = f"> {task.content}".strip()
		
		if task.scheduler is not None:
			new_line = f"{task.scheduler.code} " + new_line
		
		if task.priority != 0:
			new_line = f"{{{task.priority}}} " + new_line
		
		indent_level = len(task.id) - 1
		new_line = self.indent_char * indent_level + new_line
		line_num = prev_task.line_num if prev_task else 0
		
		if prev_task and prev_task not in (task.fts, task.parent):
			line_num += len(flatten_subtasks(prev_task))
		
		lines.insert(line_num, new_line)
		self.value = "\n".join(lines).strip() + "\n"
		
		return line_num
	
	def remove_task(self, task: Task) -> None:
		lines = self.value.splitlines()
		indent_level = len(task.id) - 1
		subtasks_count = 0
		
		for line in lines[task.line_num:]:
			if line.startswith(self.indent_char * (indent_level + 1)):
				subtasks_count += 1
			else:
				break
		
		new_value = lines[:task.line_num - 1] + lines[task.line_num + subtasks_count:]  # noqa E501
		self.value = "\n".join(new_value).strip() + "\n"


# Circular Imports
from fts.core.scheduler import Scheduler  # noqa E402
