from utils import stringToDict
from core.exceptions import InvalidSyntax
from typing import Any, List, Dict, Optional, Callable


class Task:
	
	def __init__(
		self, content: str, *,
		priority: int = 0, scheduler: Optional[Callable[[], bool]] = None
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
					subtask = Task(
						self._get_content(line),
						priority=self._get_priority(line)
					)
					
					set_subtasks(subtask, hanging_lines)
					subtasks.append(subtask)
				
				task.subtasks = subtasks
			
			task = Task(
				self._get_content(line),
				priority=self._get_priority(line)
			)
			
			set_subtasks(task, hanging_lines)
			tasks.append(task)
		
		return tasks
	
	def _get_content(self, line: str) -> str:
		for index, char in enumerate(line):
			if char == ">":
				return line[index + 1:].strip()
		
		raise InvalidSyntax()
	
	def _get_priority(self, line: str) -> int:
		for index, char in enumerate(line):
			if char == ">":
				return 0
			
			if char == "{":
				priority = "0"
				
				for char in line[index + 1:]:
					if char == "}":
						break
					
					priority += char
				
				return int(priority)
		
		raise InvalidSyntax()
