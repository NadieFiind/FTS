from typing import Any, Dict, Final
from datetime import datetime as dt


WEEK_DAYS: Final = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def stringToDict(string: str, *, indent: str = "	") -> Dict[str, Any]:
	"""Converts the {string} into `dict` based on its indentation."""
	
	def outdent(string: str, *, indent: str = "	") -> str:
		"""
			Outdent the {string}.
			When the loop encounters a line withount indent, it will break.
		"""
		result = ""
		
		for line in string.splitlines():
			if line and line[0] == indent:
				result += f"{line[1:]}\n"
			else:
				break
		
		return result
	
	result: Dict[str, Any] = {}
	line_pos = 0
	prev_key = ""
	
	for line_num, line in enumerate(string.splitlines()):
		# Filter out blank lines.
		if line.isspace():
			continue
		
		line_pos += 1
		
		# If the first non-empty line is already indented, raise an error.
		if line_pos == 1 and line[0] == indent:
			raise IndentationError(f"Unexpected indent at line {line_num}.")
		
		if line and line[0] == indent:
			# Skip if this line is already stored in the {result}.
			if result[prev_key] != {}:
				continue
			
			relevant_lines = "\n".join(string.splitlines()[line_num:])
			result[prev_key] = stringToDict(
				outdent(relevant_lines, indent=indent),
				indent=indent
			)
		else:
			result[line] = {}
			prev_key = line
	
	return result


def dateTimeToFriendlyString(datetime: dt) -> str:
	remaining_days = (datetime - datetime_now()).days
	
	if 0 <= remaining_days < 7:
		return datetime.strftime("%a %H:%M")
	
	return datetime.strftime("%Y-%m-%d %H:%M")


def datetime_now() -> dt:
	return dt.now()
