from typing import Any, Dict, Final
from datetime import datetime as dt


WEEK_DAYS: Final = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
MONTHS: Final = [
	"JAN", "FEB", "MAR", "APR", "MAY", "JUN",
	"JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
]


def stringToDict(string: str, *, indent: str = "	") -> Dict[str, Any]:
	"""Converts the {string} into `dict` based on the {indent}."""
	
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
	
	result: Dict[str, Any] = {}
	line_pos = 0  # Current line position. Empty lines are skipped.
	prev_key = ""  # The previous key stored in the [result].
	
	for line_num, line in enumerate(string.splitlines()):
		# Filter-out blank lines.
		if line.isspace():
			continue
		
		line_pos += 1
		
		# If the first non-empty line is already indented, raise an error.
		if line_pos == 1 and line.startswith(indent):
			raise IndentationError(f"Unexpected indent at line {line_num}.")
		
		if line.startswith(indent):
			# Skip if this line is already stored in the `result[prev_key]`.
			if result[prev_key] != {}:
				continue
			
			# Remove unrelevant lines.
			relevant_lines = "\n".join(string.splitlines()[line_num:])
			
			# Set the value of the `result[prev_key]` recursively.
			result[prev_key] = stringToDict(
				outdent(relevant_lines, indent=indent),
				indent=indent
			)
		else:
			# Store this line in the {result} with empty value.
			result[line] = {}
			prev_key = line
	
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
