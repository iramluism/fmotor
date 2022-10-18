from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem


from src.seedwork.ui.components import IComponent


class TabComponent(MDFloatLayout, MDTabsBase):
	pass


class MotorControlFormComponent(IComponent):

	def on_tab_switch(self, *args):
		pass

	def render(self):
		tabs = MDTabs(id="form_control")

		motor_data_tab = TabComponent(
			MotorDataTabComponent.build(), title="Motor Data")

		load_data_tab = TabComponent(
			LoadDataTabComponent.build(), title="Load Data")

		tabs.add_widget(load_data_tab)
		tabs.add_widget(motor_data_tab)
		return tabs


class MotorDataTabComponent(IComponent):

	def render(self):
		return MDGridLayout(MDTextField())


class LoadDataTabComponent(IComponent):

	def render(self):

		layout = MDGridLayout(cols=2, spacing=10, size_hint_y=None)
		layout.bind(minimum_height=layout.setter('height'))

		layout.add_widget(MDLabel(text="Field 1", halign="center"))
		layout.add_widget(MDTextField())

		layout.add_widget(MDLabel(text="Field 1", halign="center"))
		layout.add_widget(MDTextField())

		scroll = MDScrollView()

		scroll.add_widget(layout)

		return scroll


class ReadingTypeInputComponent(IComponent):

	def render(self):
		label = MDLabel(text="Reading Type")
		button = MDTextField()

		layout = MDGridLayout(cols=2)
		layout.add_widget(label)
		layout.add_widget(button)

		return layout


class IconListItem(OneLineIconListItem):
	icon = StringProperty()


class DropDownMenuInputComponent(IComponent):

	def __init__(self, items):
		super().__init__()

		self.items = items or []
		self.menu = None

	def on_press_item(self, *args):
		if self.menu:
			self.menu.open()

	def render(self):
		drop_down_item = DropDownItemInputComponent.build()
		drop_down_item.bind(on_release=self.on_press_item)

		self.menu = MDDropdownMenu(
			caller=drop_down_item,
			position="center",
			width_mult=4,
			items=[{
				"viewclass": "OneLineIconListItem",
				"icon": "dfgdgdg",
				"text": text,
			} for text in self.items or []])

		self.menu.bind()
		return drop_down_item


class DropDownItemInputComponent(IComponent):

	def render(self):
		return """

<DropDownItemInputComponent@MDScreen>:

	MDDropDownItem:
		text: 'Item 0'

"""

