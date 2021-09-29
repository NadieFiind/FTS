from core import Task
from overrides import overrides
from typing import List, Optional
from datetime import datetime as dt
from core.scheduler import Scheduler
from utils import dateToFriendlyString


def date(start: Optional[str] = None, end: Optional[str] = None) -> Scheduler:
	start_datetime = dt.strptime(start, "%Y-%m-%d %H:%M") if start else dt.min
	end_datetime = dt.strptime(end, "%Y-%m-%d %H:%M") if end else dt.max
	
	class Date(Scheduler):
		
		@overrides
		def call(self, task: Task) -> (bool, str):
			if start_datetime <= dt.now() <= end_datetime:
				return True, self.__str__()
			
			return False, self.__str__()
		
		@overrides
		def __str__(self) -> str:
			sdt = start_datetime
			edt = end_datetime
			
			if sdt != dt.min and edt == dt.max:
				return f"Start: {dateToFriendlyString(sdt)}"
			
			if sdt == dt.min and edt != dt.max:
				return f"End: {dateToFriendlyString(edt)}"
			
			if sdt == dt.min and edt == dt.max:
				return "No Schedule"
			
			return f"{dateToFriendlyString(sdt)} - {dateToFriendlyString(edt)}"
	
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
