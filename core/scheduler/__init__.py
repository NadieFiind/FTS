from core import Task
from abc import ABC, abstractmethod
from overrides import final, EnforceOverrides


class Scheduler(ABC, EnforceOverrides):
	
	@staticmethod
	@final
	def from_code(code: str) -> "Scheduler":
		return eval(code)
	
	@abstractmethod
	def call(self, task: Task) -> (bool, str):
		raise NotImplementedError()
	
	@abstractmethod
	def __str__(self) -> str:
		raise NotImplementedError()


# Circular Imports
from core.scheduler.builtins import * # noqa E402, E261
