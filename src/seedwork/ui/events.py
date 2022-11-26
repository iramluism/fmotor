""" Events Interfaces Module """

import abc
from kivy.event import EventDispatcher


class IEvent(EventDispatcher):
	""" IEvent class """

	def __init__(self,  **kwargs):
		""" Register Event """
		self.register_event_type("on_execute")
		super().__init__(**kwargs)

	@classmethod
	def execute(cls, *args, **kwargs):
		""" Execute event """
		event = cls()
		event.dispatch("on_execute", (args, kwargs))

	def on_execute(self, values):
		""" handle event """
		self.handle(*values[0], **values[1])

	@abc.abstractmethod
	def handle(self, *args, **kwargs):
		pass
