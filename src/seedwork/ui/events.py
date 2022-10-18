from kivy.properties import Property
from kivy.event import EventDispatcher


class State(Property):

	def __init__(self, initial_state, **kwargs):
		super().__init__(initial_state, **kwargs)


class StateObserver(EventDispatcher):
	pass

