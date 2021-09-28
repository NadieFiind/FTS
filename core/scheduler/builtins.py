from core import Task
from overrides import overrides
from typing import List, Optional
from core.scheduler import Scheduler


def date(start: Optional[str] = None, end: Optional[str] = None) -> Scheduler:
	class Date(Scheduler):
		
		@overrides
		def call(self, task: Task) -> (bool, str):
			return True, self.__str__()
		
		@overrides
		def __str__(self) -> str:
			return "Date"
	
	return Date()


def days(
	days: List[str], start: Optional[str] = None, end: Optional[str] = None
) -> Scheduler:
	class Days(Scheduler):
		
		@overrides
		def call(self, task: Task) -> (bool, str):
			return True, self.__str__()
		
		@overrides
		def __str__(self) -> str:
			return "Days"
	
	return Days()
