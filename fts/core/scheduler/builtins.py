from fts.core import Task
from datetime import datetime
from overrides import overrides
from datetime import datetime as dt
from fts.core.scheduler import Scheduler
from fts.core.exceptions import InvalidSyntax
from typing import Type, List, Union, Tuple, Optional
from fts.utils import MONTHS, WEEK_DAYS, datetime_now, \
	datetimeToFriendlyString, get_week_of_month, shift_sequence


# def yearly(
# 	start: Optional[str] = None, end: Optional[str] = None
# ) -> Type[Scheduler]:
# 	start_datetime = dt.strptime(start, "%m-%d %H:%M") if start else dt.min
# 	end_datetime = dt.strptime(end, "%m-%d %H:%M") if end else dt.max
	
# 	class Yearly(Scheduler):
		
# 		@overrides  # type: ignore
# 		def call(self, task: Task) -> Tuple[bool, str]:
# 			if start_datetime <= datetime_now() <= end_datetime:
# 				return True, self.__str__()
			
# 			return False, self.__str__()
		
# 		@overrides  # type: ignore
# 		def when(self, task: Task) -> datetime:
# 			print(datetime_now().replace(year=datetime_now()))
# 			if self.call(task)[0]:
# 				return datetime_now().replace(year=datetime_now())
			
# 			if datetime_now() < start_datetime:
# 				return start_datetime.replace(year=datetime_now())
			
# 			return start_datetime.replace(year=datetime_now() + 1)
		
# 		@overrides  # type: ignore
# 		def __str__(self) -> str:
# 			dtf = datetimeToFriendlyString
# 			sdt = start_datetime
# 			edt = end_datetime
			
# 			if sdt != dt.min and edt == dt.max:
# 				return f"Start: {dtf(sdt)}"
			
# 			if sdt == dt.min and edt != dt.max:
# 				return f"End: {dtf(edt)}"
			
# 			if sdt == dt.min and edt == dt.max:
# 				return "No Schedule"
			
# 			return f"{dtf(sdt)} - {dtf(edt)}"
	
# 	return Yearly()


def days(
	days: Union[str, List[str]],
	start: Optional[str] = None,
	end: Optional[str] = None
) -> Type[Scheduler]:
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
		def when(self, task: Task) -> datetime:
			date_format = "%Y-%b-%d %H:%M:%S"
			
			now = datetime_now()
			current_day = WEEK_DAYS[now.weekday()]
			current_month = MONTHS[now.month - 1]
			week = get_week_of_month(now)
			
			if self.call(task)[0]:
				return dt.strptime(
					f"{now.year}-{current_month}-{now.day} {start_time}",
					date_format
				)
			
			for day in days:
				if day in WEEK_DAYS:
					if current_day == day:
						sday: str
						
						if datetime_now().time() < end_time:
							sday = current_day
						else:
							try:
								sday = days[days.index(day) + 1]
							except IndexError:
								sday = days[0]
						
						nday = WEEK_DAYS.index(sday) + 1
						
						return dt.strptime(
							f"{now.year}-{current_month}-{nday + 7 * (week - 1)} {start_time}",
							date_format
						)
				else:
					raise InvalidSyntax()
			
			nday = WEEK_DAYS.index(current_day)
			week_days = shift_sequence(nday, WEEK_DAYS)
			nday += week_days.index(days[0]) + 1
			
			try:
				return dt.strptime(
					f"{now.year}-{current_month}-{nday + 7 * (week - 1)} {start_time}",
					date_format
				)
			except ValueError:  # day is out of range for month
				month: str
				year: int
				
				try:
					month = MONTHS[now.month]
					year = now.year
				except IndexError:
					month = MONTHS[0]
					year = now.year + 1
				
				return dt.strptime(
					f"{year}-{month}-1 {start_time}",
					date_format
				)
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
	
	return Days()


def monthly(
	months: List[str],
	start: Optional[str] = None,
	end: Optional[str] = None
) -> Scheduler:
	months = [month.strip().upper() for month in months]
	start_datetime = dt.strptime(start, "%d %H:%M") if start else dt.min
	end_datetime = dt.strptime(end, "%d %H:%M") if end else dt.max
	
	class Monthly(Scheduler):
		
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
		def when(self, task: Task) -> datetime:
			date_format = "%Y-%m-%d %H:%M:%S"
			
			now = datetime_now()
			current_month = MONTHS[now.month - 1]
			
			if self.call(task)[0]:
				return dt.strptime(
					f"{now.year}-{now.month}-{start_datetime.strftime('%d %H:%M:%S')}",
					date_format
				)
			
			for month in months:
				if month in MONTHS:
					if current_month == month:
						smonth: str
						
						if datetime_now() < end_datetime:
							smonth = current_month
						else:
							try:
								smonth = months[months.index(month) + 1]
							except IndexError:
								smonth = months[0]
						
						nmonth = MONTHS.index(smonth) + 1
						
						return dt.strptime(
							f"{now.year}-{nmonth}-{start_datetime.strftime('%d %H:%M:%S')}",
							date_format
						)
				else:
					raise InvalidSyntax()
			
			nmonth = MONTHS.index(current_month)
			shifted_months = shift_sequence(nmonth, MONTHS)
			nmonth += shifted_months.index(months[0]) + 1
			
			try:
				return dt.strptime(
					f"{now.year}-{nmonth}-{start_datetime.strftime('%d %H:%M:%S')}",
					date_format
				)
			except ValueError:  # day is out of range for month
				return dt.strptime(
					f"{now.year + 1}-01-{start_datetime.strftime('%d %H:%M:%S')}",
					date_format
				)
		
		@overrides  # type: ignore
		def __str__(self) -> str:
			sdt = start_datetime
			edt = end_datetime
			return f"{sdt.strftime('%d %H:%M')} - {edt.strftime('%d %H:%M')}"
	
	return Monthly()
