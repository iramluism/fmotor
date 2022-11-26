""" Services Interfaces Module """

import abc


class IService(metaclass=abc.ABCMeta):
	""" IService class """

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass
