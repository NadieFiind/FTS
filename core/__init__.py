import os
from utils import stringToDict
from core.exceptions import InvalidSyntax
from typing import Any, List, Dict, Tuple, Optional


class Task:
	
	def __init__(
		self, content: str, *,
		priority: int = 0, scheduler: Optional["Scheduler"] = None
	):
		self.content = content
		self.priority = priority
		self._scheduler = scheduler
		self.subtasks: List[Task] = []
	
	def scheduler(self) -> Tuple[Optional[bool], str]:
		if self._scheduler is None:
			return None, "No Scheduler"
		
		return self._scheduler.call(self)


class FTS:
	
	def __init__(self, fts_format: str, *, indent_char: str = "	"):
		self._parser = FTSFParser(fts_format, indent_char=indent_char)
		self.tasks: List[Task] = self._parser.get_tasks()


class FTSFParser:
	
	def __init__(self, fts_format: str, *, indent_char: str = "	") -> None:
		self._fts_format = fts_format
		self._remove_empty_lines()
		self._remove_comments()
		self._indent_char = indent_char
	
	def _remove_empty_lines(self) -> None:
		self._fts_format = os.linesep.join(
			[line for line in self._fts_format.splitlines() if line]
		)
	
	def _remove_comments(self) -> None:
		result = [line.split("~#")[0] for line in self._fts_format.splitlines()]
		self._fts_format = "\n".join(result)
	
	def get_tasks(self) -> List[Task]:
		tasks: List[Task] = []
		
		for line, hanging_lines in stringToDict(
			self._fts_format, indent=self._indent_char
		).items():
			def set_subtasks(task: Task, lines: Dict[str, Any]) -> None:
				subtasks: List[Task] = []
				
				for line, hanging_lines in lines.items():
					priority, scheduler = self._get_priority_and_scheduler(line)
					subtask = Task(
						self._get_content(line),
						priority=priority + task.priority,
						scheduler=scheduler or task._scheduler
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
					
					return Scheduler.from_code(scheduler_code.strip())  # type: ignore
				
				scheduler_code += char
			
			raise InvalidSyntax()
		
		return get_priority(), get_scheduler()


# Circular Imports
from core.scheduler import Scheduler # noqa E402
