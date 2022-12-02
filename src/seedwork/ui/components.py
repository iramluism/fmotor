""" Component Interfaces module """

import abc
import inject

from kivy.uix.widget import Widget

from .builder import IBuilder


class IComponent(metaclass=abc.ABCMeta):
	""" IComponent class """

	builder = inject.attr(IBuilder)
	state = {}
	widget: Widget = None

	def __getattr__(self, attr):
		if attr in dir(self.widget):
			return self.widget.__getattribute__(attr)

	def __init__(self, *args, **kwargs):
		pass

	@classmethod
	def build(cls, *args, **kwargs):
		""" Build component from builder """
		component = cls(*args, **kwargs)
		widget = cls.builder.build_component(component)

		widget.component = component
		component.widget = widget

		return component.widget

	@abc.abstractmethod
	def render(self):
		pass

