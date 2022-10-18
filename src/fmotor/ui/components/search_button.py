
import inspect

from src.seedwork.ui.components import IComponent

from kivymd.uix.button import MDFloatingActionButtonSpeedDial


class FloatButtonComponent(IComponent):

	def __init__(self, search_action=None, calculate_action=None,
	             estimate_action=None):
		super().__init__()

		self.actions = {
			"magnify": ["Search", search_action],
			"estimate": ["Estimate", estimate_action],
			"calculator": ["Calculate", calculate_action]
		}

		self.search_action = search_action
		self.calculate_action = calculate_action
		self.estimate_action = estimate_action

	def callback(self, button):
		self.close_stack()
		action = self.actions.get(button.icon)[1]
		if inspect.isfunction(action) or inspect.ismethod(action):
			action()

	def render(self):

		button = MDFloatingActionButtonSpeedDial(
			pos_hint={'x': .8, 'y': .05},
			root_button_anim=True,
			data={
				label: icon for icon, (label, action) in self.actions.items()
			},
			label_text_color=(1, 1, 1, 1),
			color_icon_root_button=(1, 1, 1, 1),
			color_icon_stack_button=(1, 1, 1, 1),
			callback=self.callback
		)

		return button
