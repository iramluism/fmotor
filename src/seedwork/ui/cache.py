""" Cache Interfaces Module """

from kivy.cache import Cache
from typing import Any, ClassVar, Optional


class ICache:
	""" ICache class """

	_cache: ClassVar = Cache
	cache_name: str = None

	def __init__(self):

		if not self.cache_name:
			self.cache_name = self.__class__.__name__

		if self.cache_name not in self._cache._categories:
			self._cache.register(self.cache_name)

	def set(self, key: str, value: Any):
		self._cache.append(self.cache_name, key, value)

	def get(self, key: str, default_value: Optional[Any] = None):
		return self._cache.get(self.cache_name, key) or default_value

	def remove(self, key: str):
		self._cache.remove(self.cache_name, key)


class ComponentCache(ICache):
	pass


class EventCache(ICache):
	pass


class TranslatorCache(ICache):
	pass
