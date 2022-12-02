""" Builder Interfaces Module """

import abc
import inspect
import inject

from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget

from .cache import ComponentCache


class IBuilder(metaclass=abc.ABCMeta):
	""" IBuilder class """

	_component_cache = inject.attr(ComponentCache)
	_builder = Builder

	def load_file(self, *args, **kwargs):
		""" Load widget from kv file """
		return self._builder.load_file(*args, **kwargs)

	def get_component(self, comp_id):
		""" Get Component from cache """
		return self._component_cache.get(comp_id)

	@staticmethod
	def get_events_from_states(component):
		""" Get events and methods from the rendered widget"""

		states = component.state
		component.observers = {}
		events = {}
		methods = {}

		for attr in dir(component):

			if inspect.ismethod((method := component.__getattribute__(attr))):

				if attr.startswith("on_"):

					state_name = attr[3:]
					if state_name in states:
						events.update({state_name: method})
					else:
						events[attr] = method

				elif not attr.startswith(("_", "__")):
					methods.update({attr: method})

		return events, methods

	def build_component(self, component):
		""" Build Component and save it on cache """

		widget = None
		content = component.render()

		if isinstance(content, Widget):
			widget = content

		if not widget:
			Builder.load_string(content)
			widget = Factory.get(component.__class__.__name__)()

		events, methods = self.get_events_from_states(component)
		widget.__dict__.update(methods)
		widget.bind(**events)

		if component.id:
			self._component_cache.set(component.id, component)

		return widget

