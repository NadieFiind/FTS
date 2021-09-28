from utils import stringToDict
from core.exceptions import InvalidSyntax
from typing import Any, List, Dict, Optional, Callable


class Task:
	
	def __init__(
		self, content: str, *,
		priority: int = 0, scheduler: Optional[Callable[["Task"], bool]] = None
	):
		self.content = content
		self.priority = priority
		self.scheduler = scheduler
		self.subtasks: List[Task] = []


class FTS:
	
	def __init__(self, fts_format: str):
		self._data = FTSData(fts_format)
		self.tasks: List[Task] = self._data.get_tasks()


class FTSData:
	
	def __init__(self, fts_format: str) -> None:
		self._fts_format = fts_format
	
	def get_tasks(self) -> List[Task]:
		tasks: List[Task] = []
		
		for line, hanging_lines in stringToDict(self._fts_format).items():
			def set_subtasks(task: Task, lines: Dict[str, Any]) -> None:
				subtasks: List[Task] = []
				
				for line, hanging_lines in lines.items():
					priority, scheduler = self._get_priority_and_scheduler(line)
					subtask = Task(
						self._get_content(line), priority=priority, scheduler=scheduler
					)
					
					set_subtasks(subtask, hanging_lines)
					subtasks.append(subtask)
				
				task.subtasks = subtasks
			
			priority, scheduler = self._get_priority_and_scheduler(line)
			task = Task(self._get_content(line), priority=priority, scheduler=scheduler)
			
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
	) -> (int, Optional[Callable[[Task], bool]]):
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
		
		def get_scheduler() -> Optional[Callable[[Task], bool]]:
			scheduler_code = ""
			
			for index, char in enumerate(line[cursor:]):
				if char == ">":
					return schedulers.parse(scheduler_code)
				
				scheduler_code += char
			
			raise InvalidSyntax()
		
		return get_priority(), get_scheduler()


from core import schedulers # noqa E402
