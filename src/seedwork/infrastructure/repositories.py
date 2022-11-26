""" Repositories Interfaces Module """

import abc


class IRepository(metaclass=abc.ABCMeta):
	""" IRepository class """

	def filter(self, *args, **kwargs):
		pass

	def all(self, *args, **kwargs):
		pass

	def save(self, *args, **kwargs):
		pass

	def get(self, *args, **kwargs):
		pass
