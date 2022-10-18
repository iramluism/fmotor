
import abc

from kivy.uix.widget import Widget
from dependency_injector.wiring import Provide

from src.seedwork.ui.utils import get_running_app


class IComponent:
	__metaclass__ = abc.ABCMeta

	builder = Provide["builder"]
	state = {}
	widget: Widget = None

	def get_component_by_id(self, _id):
		pass

	def __getattr__(self, attr):
		if attr in dir(self.widget):
			return self.widget.__getattribute__(attr)

	def __init__(self, *args, **kwargs):
		pass

	@classmethod
	def build(cls, *args, **kwargs):
		component = cls(*args, **kwargs)
		widget = cls.builder.build_component(component)
		widget.component = component
		component.widget = widget
		return component.widget

	@abc.abstractmethod
	def render(self):
		pass

