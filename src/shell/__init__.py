import os
import json
from typing import List
from core import FTS, Task


def initialize_fts() -> FTS:
	with open("config.json") as file:
		config = json.load(file, strict=False)
	
	with open("core/data/data.json") as file:
		data = json.load(file)
	
	home_ftsf_path = os.path.join(config["ftsf_folder"], data["home_ftsf"])
	
	try:
		with open(home_ftsf_path) as file:
			return FTS(file.read(), indent_char=config.get("indent_char"))
	except FileNotFoundError:
		os.makedirs(config["ftsf_folder"], exist_ok=True)
		
		with open("core/data/ftsf/default.ftsf") as file:
			ftsf = file.read()
		
		with open(home_ftsf_path, "w") as file:
			file.write(ftsf)
			return FTS(ftsf, indent_char=config.get("indent_char"))


def print_tasks(tasks: List[Task], *, indent_level: int = 0) -> None:
	tasks.sort(key=lambda task: task.priority, reverse=True)
	
	for task in tasks:
		do_now, _ = task.scheduler()
		
		if do_now or do_now is None:
			if task.priority >= 0:
				if task.subtasks:
					print(f"{'  ' * indent_level}\033[1m{task.content}\033[0m")
				else:
					print(f"{'  ' * indent_level}{task.content}")
			else:
				print(f"{'  ' * indent_level}\033[2m{task.content}\033[0m")
			
			print_tasks(task.subtasks, indent_level=indent_level + 1)


def main() -> None:
	fts = initialize_fts()
	print_tasks(fts.tasks)
