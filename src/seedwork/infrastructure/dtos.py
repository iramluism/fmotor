
from dataclasses import dataclass, asdict


@dataclass
class IDTO:
	""" Abstract DTO """

	def as_dict(self):
		""" Serializer object
		:return: dict format
		"""
		return asdict(self)

	def get(self, field):
		return self.__getattribute__(field)

	def set(self, field, value):
		return self.__setattr__(field, value)
