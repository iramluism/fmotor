""" Queries Interfaces Module """

import abc


class IQuery(metaclass=abc.ABCMeta):
	""" IQuery class """

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass
