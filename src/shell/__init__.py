import os
import json
from typing import List
from core import FTS, Task


def initialize_fts() -> FTS:
	# Open the configuration data.
	with open("config.json") as file:
		config = json.load(file, strict=False)
	
	# Open the data file.
	with open("core/data/data.json") as file:
		data = json.load(file)
	
	# The path of the home FTS format file.
	home_ftsf_path = os.path.join(config["ftsf_folder"], data["home_ftsf"])
	
	try:
		# Initialize the {FTS} from the home FTS format file.
		with open(home_ftsf_path) as file:
			return FTS(file.read(), indent_char=config.get("indent_char"))
	
	# If the home FTS format file doesn't exist, create one.
	except FileNotFoundError:
		os.makedirs(config["ftsf_folder"], exist_ok=True)
		
		with open("core/data/ftsf/default.ftsf") as file:
			ftsf = file.read()
		
		with open(home_ftsf_path, "w") as file:
			file.write(ftsf)
			return FTS(ftsf, indent_char=config.get("indent_char"))


def print_tasks(tasks: List[Task], *, indent_level: int = 0) -> None:
	# Sort the shallow copy of the {task} by prioriry.
	tasks[:].sort(key=lambda task: task.priority, reverse=True)
	
	for task in tasks:
		do_now, _ = task.scheduler()
		
		# Show the tasks that must be done now and the tasks that has no scheduler.
		if do_now or do_now is None:
			if task.priority >= 0:
				# If the {task} has subtasks, make the text bold.
				if task.subtasks:
					print(f"{'  ' * indent_level}\033[1m{task.content}\033[0m")
				# Otherwise, normal text.
				else:
					print(f"{'  ' * indent_level}{task.content}")
			
			# If the {task}'s priority is -1, make the text gray.
			else:
				print(f"{'  ' * indent_level}\033[2m{task.content}\033[0m")
			
			# Recursively print the subtasks of the {task}.
			print_tasks(task.subtasks, indent_level=indent_level + 1)


def main() -> None:
	"""Entry Point"""
	fts = initialize_fts()
	print_tasks(fts.tasks)
