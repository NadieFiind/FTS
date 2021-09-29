from core import Task
from overrides import overrides
from datetime import datetime as dt
from core.scheduler import Scheduler
from typing import List, Tuple, Optional
from core.exceptions import InvalidSyntax
from utils import week_days, datetime_now, dateTimeToFriendlyString


def date(start: Optional[str] = None, end: Optional[str] = None) -> Scheduler:
	start_datetime = dt.strptime(start, "%Y-%m-%d %H:%M") if start else dt.min
	end_datetime = dt.strptime(end, "%Y-%m-%d %H:%M") if end else dt.max
	
	class Date(Scheduler):
		
		@overrides  # type: ignore
		def call(self, task: Task) -> Tuple[bool, str]:
			if start_datetime <= datetime_now() <= end_datetime:
				return True, self.__str__()
			
			return False, self.__str__()
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			dtf = dateTimeToFriendlyString
			sdt = start_datetime
			edt = end_datetime
			
			if sdt != dt.min and edt == dt.max:
				return f"Start: {dtf(sdt)}"
			
			if sdt == dt.min and edt != dt.max:
				return f"End: {dtf(edt)}"
			
			if sdt == dt.min and edt == dt.max:
				return "No Schedule"
			
			return f"{dtf(sdt)} - {dtf(edt)}"
	
	return Date()


def days(
	days: List[str], start: Optional[str] = None, end: Optional[str] = None
) -> Scheduler:
	start_time = dt.strptime(start, "%H:%M").time() if start else dt.min.time()
	end_time = dt.strptime(end, "%H:%M").time() if end else dt.max.time()
	
	class Days(Scheduler):
		
		@overrides  # type: ignore
		def call(self, task: Task) -> Tuple[bool, str]:
			current_day = week_days[datetime_now().weekday()]
			
			for day in days:
				day = day.strip().upper()
				
				if day in week_days:
					if current_day == day:
						if start_time <= datetime_now().time() <= end_time:
							return True, self.__str__()
				else:
					raise InvalidSyntax()
			
			return False, self.__str__()
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
	
	return Days()
