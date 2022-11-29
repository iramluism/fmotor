""" DTO Interfaces Module """

from dataclasses import dataclass, asdict, fields
from typing import NoReturn, Any, List, Optional


@dataclass
class IDTO:
	""" Abstract DTO """

	def as_dict(self):
		""" Serializer object
		:return: dict format
		"""
		return asdict(self)

	def get(self, field: str, default_value: Optional[Any] = None) -> Any:
		return getattr(self, field, default_value)

	def set(self, field: str, value: Any) -> NoReturn:
		self.__setattr__(field, value)

	@classmethod
	def fields(cls) -> List[str]:
		""" Get all fields of the DTO """
		return [field.name for field in fields(cls)]
