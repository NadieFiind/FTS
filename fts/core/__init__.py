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
		self.content = content
		self.priority = priority
		self.scheduler = scheduler
		self.subtasks: List[Task] = []
		self.line_num = line_num  # Line number of this task in the FTS format file.
	
	@property
	def sorted_subtasks(self) -> List["Task"]:
		"""Key: priority * int(scheduler[0]) * 2"""
		return sorted(
			self.subtasks,
			key=lambda task: task.priority + int(task.call_scheduler()[0] or 0) * 2,
			reverse=True
		)
	
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
		self.tasks: List[Task] = self._parser.get_tasks(self)
	
	@property
	def sorted_tasks(self) -> List[Task]:
		"""Key: priority * int(scheduler[0]) * 2"""
		return sorted(
			self.tasks,
			key=lambda task: task.priority + int(task.call_scheduler()[0] or 0) * 2,
			reverse=True
		)
	
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


# Circular Imports
from fts.core.scheduler import Scheduler  # noqa E402
