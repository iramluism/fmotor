
from src.seedwork.ui.components import IComponent
from kivymd.uix.textfield import MDTextField


class MotorFieldComponent(IComponent):

	def __init__(self):
		super().__init__()

		self.hint_text = "Helper"
		self.helper_text = "Helper text"

	def render(self):
		return MDTextField()
