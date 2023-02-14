""" Events Interfaces Module """

import abc
from kivy.clock import Clock

import inject

from .cache import EventCache


class IEvent:
	""" IEvent class """

	cid = None
	_event_cache = inject.attr(EventCache)

	@classmethod
	def dispatch(cls, *args, timeout=0, **kwargs):
		""" Dispatch event """

		event = Clock.schedule_once(
			lambda e: cls.handle(cls(), *args, **kwargs), timeout)
		
		cls._event_cache.set(cls.get_cid(), event)

	@classmethod
	def get_cid(cls):
		return cls.cid or cls.__name__.lower()

	@classmethod
	def cancel(cls):
		event = cls._event_cache.get(cls.get_cid())
		event.cancel()

	@abc.abstractmethod
	def handle(self, *args, **kwargs):
		""" Handle event """
