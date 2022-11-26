""" View Model Interfaces Module """

import abc


class IViewModel(metaclass=abc.ABCMeta):
	""" IViewModel class """

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass
