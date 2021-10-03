from collections import OrderedDict
from datetime import datetime as dt
from typing import Any, Dict, Final, Tuple


WEEK_DAYS: Final = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
MONTHS: Final = [
	"JAN", "FEB", "MAR", "APR", "MAY", "JUN",
	"JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
]


def stringToDict(
	string: str, *, indent: str = "	", starting_line_num: int = 1
) -> Dict[Tuple[int, str], Any]:
	"""Converts the {string} into `dict` based on the {indent}."""
	
	result: Dict[Tuple[int, str], Any] = OrderedDict()
	line_num: int = starting_line_num - 1  # Current line number.
	line_pos: int = 0  # Current line position. Empty lines are skipped.
	prev_key: Tuple[int, str] = (-1, "")  # Previous key stored in the {result}.
	
	def outdent(string: str, *, indent: str = "	") -> str:
		"""
			Outdent the {string}.
			When the loop encounters a line withount indent, it will break.
		"""
		result = ""
		
		for line in string.splitlines():
			if line.startswith(indent):
				result += f"{line[1:]}\n"
			else:
				break
		
		return result
	
	for index, line in enumerate(string.splitlines()):
		line_num += 1
		
		if not line.isspace():
			line_pos += 1
		
		# If the first non-empty line is already indented, raise an error.
		if line_pos == 1 and line.startswith(indent):
			raise IndentationError(f"Unexpected indent at line {line_num}.")
		
		if line.startswith(indent) and not line.isspace():
			# Skip if this line is already stored in the `result[prev_key]`.
			if result[prev_key] != {}:
				continue
			
			# Remove unrelevant lines.
			relevant_lines = "\n".join(string.splitlines()[index:])
			
			# Set the value of the `result[prev_key]` recursively.
			result[prev_key] = stringToDict(
				outdent(relevant_lines, indent=indent),
				indent=indent,
				starting_line_num=line_num
			)
		else:
			# Store this line in the {result} with empty value.
			result[(line_num, line)] = {}
			prev_key = (line_num, line)
	
	return result


def datetimeToFriendlyString(datetime: dt) -> str:
	"""
		Convert the {datetime} into a readable string format.
		If the {datetime} is in less than a week,
		the date will be replaced by day. (e.g. "2021-09-26" -> "Sun")
	"""
	remaining_days = (datetime - datetime_now()).days
	
	if 0 <= remaining_days < 7:
		return datetime.strftime("%a %H:%M")
	
	return datetime.strftime("%Y-%m-%d %H:%M")


def datetime_now() -> dt:
	return dt.now()
