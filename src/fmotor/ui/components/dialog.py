""" Fmotor Dialog Component Module """

from src.seedwork.ui.components import IComponent
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarListItem
from kivy.core.clipboard import Clipboard
from kivymd.uix.button import MDIconButton


class MotorItemDialogComponent(IComponent):
	""" MotorItemDialogComponent class """

	def __init__(self, motor_id, text=None, secondary_text=None):
		super().__init__()

		self.id = motor_id
		self.text = text
		self.secondary_text = secondary_text

	def render(self):
		return TwoLineAvatarIconListItem(text=self.text,
		                                 secondary_text=self.secondary_text)


class FilterMotorDialogComponent(IComponent):
	""" DialogComponent class """

	def __init__(self, items=None):
		super().__init__()
		self.items = items or []

	def render(self):
		return MDDialog(title="Motors", type="simple",
		                items=self.items, width_offset="12")


class MotorDetailDialogComponent(IComponent):
	""" MotorDetailDialogComponent class """

	def __init__(self, motor_details: dict):
		super().__init__()
		self.motor_details = motor_details

	def copy_property_on_clipboard(self):
		text = "\n".join("%s: %s" % (field, value)
		                 for field, value in self.motor_details.items())

		Clipboard.copy(text)

	def render(self):
		model = self.motor_details.get("model")

		dialog = MDDialog(
			title=model,
			width_offset="24dp",
			type="simple",
			items=[
				OneLineAvatarListItem(text="[b] %s :[/b] %s" % (field, value))
				for field, value in self.motor_details.items()
			],
			buttons=[
				MDIconButton(icon="share-variant-outline"),
				MDIconButton(icon="content-copy")
			])

		return dialog

