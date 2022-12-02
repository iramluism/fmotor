""" Repositories Interfaces Module """

import abc
import inject

from .database import SQLiteManager


class IRepository(metaclass=abc.ABCMeta):
	""" IRepository class """

	db = inject.attr(SQLiteManager)

	def filter(self, *args, **kwargs):
		pass

	def all(self, *args, **kwargs):
		pass

	def save(self, *args, **kwargs):
		pass

	def get(self, *args, **kwargs):
		pass
