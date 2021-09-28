from core import Task
from typing import List, Callable, Optional


def parse(code: str) -> Callable[[Task], bool]:
	exec(code.strip())


def date(start: Optional[str] = None, end: Optional[str] = None) -> bool:
	print(start, end)


def days(
	days: List[str], start: Optional[str] = None, end: Optional[str] = None
) -> bool:
	print(days, start, end)
