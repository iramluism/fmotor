""" Entities Interface Module """

import abc
import dataclasses
from typing import List, Any, NoReturn
from dataclasses import asdict, fields


@dataclasses.dataclass()
class IEntity(metaclass=abc.ABCMeta):
	""" IEntity class """

	def get(self, field: str) -> Any:
		return getattr(self, field)

	def set(self, field: str, value: Any) -> NoReturn:
		setattr(self, field, value)

	def as_dict(self) -> dict:
		""" Serialize object
		:return: dict format
		"""
		return asdict(self)

	@classmethod
	def fields(cls) -> List[str]:
		""" Return all fields of the entity """
		return [field.name for field in cls.field_details()]

	@classmethod
	def field_details(cls):
		return fields(cls)


