from core import Task
from overrides import overrides
from datetime import datetime as dt
from core.scheduler import Scheduler
from core.exceptions import InvalidSyntax
from typing import List, Union, Tuple, Optional
from utils import MONTHS, WEEK_DAYS, datetime_now, datetimeToFriendlyString


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
			dtf = datetimeToFriendlyString
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
	days: Union[str, List[str]],
	start: Optional[str] = None,
	end: Optional[str] = None
) -> Scheduler:
	if isinstance(days, str):
		if days.lower() == "everyday":
			days = WEEK_DAYS
		elif days.lower() == "weekdays":
			days = ["MON", "TUE", "WED", "THU", "FRI"]
		elif days.lower() == "weekends":
			days = ["SAT", "SUN"]
	
	days = [day.strip().upper() for day in days]
	start_time = dt.strptime(start, "%H:%M").time() if start else dt.min.time()
	end_time = dt.strptime(end, "%H:%M").time() if end else dt.max.time()
	
	class Days(Scheduler):
		
		@overrides  # type: ignore
		def call(self, task: Task) -> Tuple[bool, str]:
			current_day = WEEK_DAYS[datetime_now().weekday()]
			
			for day in days:
				if day in WEEK_DAYS:
					if current_day == day:
						if start_time <= datetime_now().time() <= end_time:
							return True, self.__str__()
						
						return False, f"Today: {self.__str__()}"
				else:
					raise InvalidSyntax()
			
			return False, f"{', '.join(days)}: {self.__str__()}"
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
	
	return Days()


def months(
	months: List[str],
	start: Optional[str] = None,
	end: Optional[str] = None
) -> Scheduler:
	months = [month.strip().upper() for month in months]
	start_datetime = dt.strptime(start, "%d %H:%M") if start else dt.min
	end_datetime = dt.strptime(end, "%d %H:%M") if end else dt.max
	
	class Months(Scheduler):
		
		@overrides  # type: ignore
		def call(self, task: Task) -> Tuple[bool, str]:
			current_month = MONTHS[datetime_now().month - 1]
			
			for month in months:
				if month in MONTHS:
					if current_month == month:
						if start_datetime <= datetime_now() <= end_datetime:
							return True, self.__str__()
						
						return False, f"This Month: {self.__str__()}"
				else:
					raise InvalidSyntax()
			
			return False, f"{', '.join(months)}: {self.__str__()}"
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			sdt = start_datetime
			edt = end_datetime
			return f"{sdt.strftime('%d %H:%M')} - {edt.strftime('%d %H:%M')}"
	
	return Months()
