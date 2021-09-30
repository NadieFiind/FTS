from core import Task
from typing import Tuple
from abc import ABC, abstractmethod
from overrides import final, EnforceOverrides


class Scheduler(ABC, EnforceOverrides):  # type: ignore
	
	@staticmethod
	@final  # type: ignore
	def from_code(code: str) -> "Scheduler":
		return eval(code)  # type: ignore
	
	@abstractmethod
	def call(self, task: Task) -> Tuple[bool, str]:
		raise NotImplementedError()
	
	@abstractmethod
	def __str__(self) -> str:
		raise NotImplementedError()


# Circular Imports
from core.scheduler.builtins import *  # noqa E402, E261
