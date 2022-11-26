""" Command Interface Module """

import abc


class ICommand(metaclass=abc.ABCMeta):
	""" ICommand class """

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass
