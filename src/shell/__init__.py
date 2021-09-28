import os
from typing import List
from core import FTS, Task


def main() -> None:
	try:
		with open("data/tasks.ftsf") as file:
			fts = FTS(file.read())
	except FileNotFoundError:
		os.makedirs("data", exist_ok=True)
		
		with open("core/data/default_tasks.ftsf") as file:
			default_tasks = file.read()
		
		with open("data/tasks.ftsf", "w") as file:
			file.write(default_tasks)
			fts = FTS(default_tasks)
	
	def show(tasks: List[Task], *, level: int = 0) -> None:
		tasks.sort(key=lambda task: task.priority, reverse=True)
		
		for task in tasks:
			print(f"{'  ' * level}{task.content}")
			show(task.subtasks, level=level + 1)
	
	show(fts.tasks)
