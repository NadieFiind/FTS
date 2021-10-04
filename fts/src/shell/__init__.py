from typing import List
from fts.core import Task
from fts.data_handler import initialize_fts


def print_tasks(tasks: List[Task], *, indent_level: int = 0) -> None:
	# Sort the shallow copy of the {task} by prioriry.
	tasks[:].sort(key=lambda task: task.priority, reverse=True)
	
	for task in tasks:
		do_now, _ = task.call_scheduler()
		
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
