from typing import Tuple
from fts.core import Task
from abc import ABC, abstractmethod
from overrides import final, EnforceOverrides


class Scheduler(ABC, EnforceOverrides):
	
	@final  # type: ignore
	def __init__(self) -> None:
		self.code: str
	
	@staticmethod
	@final  # type: ignore
	def from_code(code: str) -> "Scheduler":
		scheduler: Scheduler = eval(code)
		scheduler.code = code
		return scheduler
	
	@abstractmethod
	def call(self, task: Task) -> Tuple[bool, str]:
		raise NotImplementedError()
	
	@abstractmethod
	def __str__(self) -> str:
		raise NotImplementedError()


# Circular Imports
from fts.core.scheduler.builtins import *  # noqa E402, E261
