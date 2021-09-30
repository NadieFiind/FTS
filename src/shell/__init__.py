import os
import json
from typing import List
from core import FTS, Task


def main() -> None:
	with open("config.json") as file:
		config = json.load(file)
	
	with open("core/data/data.json") as file:
		data = json.load(file)
	
	home_ftsf_path = os.path.join(config["ftsf_folder"], data["home_ftsf"])
	
	try:
		with open(home_ftsf_path) as file:
			fts = FTS(file.read())
	except FileNotFoundError:
		os.makedirs(config["ftsf_folder"], exist_ok=True)
		
		with open("core/data/ftsf/default.ftsf") as file:
			default_tasks = file.read()
		
		with open(home_ftsf_path, "w") as file:
			file.write(default_tasks)
			fts = FTS(default_tasks)
	
	def show(tasks: List[Task], *, level: int = 0) -> None:
		tasks.sort(key=lambda task: task.priority, reverse=True)
		
		for task in tasks:
			print(f"{'  ' * level}{task.content}")
			show(task.subtasks, level=level + 1)
	
	show(fts.tasks)
