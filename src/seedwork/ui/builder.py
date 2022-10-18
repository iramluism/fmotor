
import abc
import inspect

from src.seedwork.ui.components import IComponent
from kivy.lang.builder import Builder
from kivy.factory import Factory
from src.seedwork.ui.utils import get_state, get_running_app


from kivy.uix.widget import Widget


class IBuilder(metaclass=abc.ABCMeta):

	@property
	def app(self):
		return get_running_app()

	def __init__(self):
		self._builder = Builder

	def parse_state_name(self, event_name):
		return event_name[3:]

	def get_events_from_states(self, component: IComponent):

		states = component.state
		component.observers = observers = {}
		events = {}
		methods = {}

		for attr in dir(component):

			if inspect.ismethod((method := component.__getattribute__(attr))):

				if attr.startswith("on_"):

					state = self.parse_state_name(attr)
					if state in states:
						initial_value = states.get(state)
						state, event = get_state(initial_value)
						observers.update({state: get_state(initial_value)})
						events.update({state: method})
					else:
						events[attr] = method

				elif not attr.startswith(("_", "__")):
					methods.update({attr: method})

		return events, methods

	def build_component(self, component: IComponent, **kwargs):

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
		component.app = self.app
		return widget

