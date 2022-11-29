""" Events Interfaces Module """

import abc
from kivy.clock import Clock


class IEvent:
	""" IEvent class """

	@classmethod
	def dispatch(cls, *args, **kwargs):
		""" Dispatch event """
		event = cls()
		Clock.schedule_once(lambda e: cls.handle(event, *args, **kwargs), 0)

	@abc.abstractmethod
	def handle(self, *args, **kwargs):
		""" Handle event """
