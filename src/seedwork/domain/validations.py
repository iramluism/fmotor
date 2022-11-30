""" Validator Interfaces module """

import abc
import copy

from typing import NoReturn


class IValidator(metaclass=abc.ABCMeta):
	""" IValidator class """

	_error_context = []

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass

	def add_error(self, message: str) -> NoReturn:
		""" add error message to context """

		self._error_context.append(
			{
				"type": "Error",
				"message": message,
				"reference": self.__class__.__name__
			}
		)

	def clear_context(self):
		self._error_context.clear()

	def is_valid(self) -> bool:
		return not self._error_context

	def raise_errors(self) -> NoReturn:
		errors = copy.deepcopy(self._error_context)
		self.clear_context()
		raise TypeError(errors)
