""" Repositories Interfaces Module """

import abc
from dependency_injector.wiring import Provide


class IRepository(metaclass=abc.ABCMeta):
	""" IRepository class """

	db = Provide["db"]

	def filter(self, *args, **kwargs):
		pass

	def all(self, *args, **kwargs):
		pass

	def save(self, *args, **kwargs):
		pass

	def get(self, *args, **kwargs):
		pass
