""" Fmotor UI Components Module """

from typing import List, Optional, NoReturn

from dependency_injector.wiring import Provide
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, IconLeftWidget
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (
	MDFlatButton,
	MDFloatingActionButton,
	MDIconButton
)

from src.fmotor.ui.utils import prepare_motor_values
from src.seedwork.ui.components import IComponent


class FMotorAppComponent(IComponent):
	""" FMotorAppComponent class """

	def render(self) -> MDScreen:
		""" Render the main app. Setup all skeleton and init
		necessary components to improve the performance. This component
		spend some time rendering some widgets.
		"""

		MotorFormComponent.build()
		MotorComponent.build()
		EstimateMotorComponent.build()

		root = MDScreen(
			MDFloatLayout(
				MDBoxLayout(
					ToolBarComponent.build(title="fMotor"),
					MDBoxLayout(
						ListMotorComponent.build(),
						orientation="vertical"),
					orientation="vertical"),
				SearchButtonComponent.build()
			)
		)

		return root


class MotorItemComponent(IComponent):
	""" MotorItemComponent class """

	def __init__(self, motor: dict):
		super().__init__()
		self.motor = motor

	def on_press(self, *args) -> NoReturn:
		""" Plot a dialog with all motor values """

		dialog = self.builder.get_component("motor")
		dialog.refresh_data(self.motor)
		dialog.open()

	def render(self) -> TwoLineAvatarIconListItem:
		""" Render Icon with a brief motor description """

		model = "%s (%s)" % (self.motor.get("model", "").lower(),
		                     self.motor.get("design"))

		description = "%s, %s, %s" % (self.motor.get("frame"),
		                              self.motor.get("catalog"),
		                              self.motor.get("manufacturer"))

		item = TwoLineAvatarIconListItem(
			IconLeftWidget(
				icon="engine"
			),
			text=model,
			secondary_text=description
		)

		return item


class SearchButtonComponent(IComponent):
	""" SearchButtonComponent class """

	def render(self):
		""" Render the floating search button """

		return MDFloatingActionButton(
			pos_hint={'x': .8, 'y': .05}, icon="magnify",
			icon_color=(1, 1, 1, 1),
			on_press=lambda e: MotorFormComponent.build().open()
		)


class ToolBarComponent(IComponent):
	""" ToolBarComponent class """

	id = "toolbar"

	def __init__(self, title, actions=None):
		super().__init__()
		self.title = title
		self.actions = actions or {}
		self.widget = MDTopAppBar(
			title=self.title, opposite_colors=True,
			md_bg_color=(1, 1, 0, 1), type_height="small", elevation=4
		)

	def update_title(self, title: str) -> NoReturn:
		""" Update toolbar title """
		self.title = title

	def restore_toolbar(self):
		self.update_actions(self.actions)
		self.update_title(self.title)

	def update_actions(self, actions: dict) -> NoReturn:
		""" Update toolbar actions """

		toolbar = self.widget

		right_actions = actions.get("right", [])
		right_actions.append(["dots-vertical", lambda e: print("menu")])
		toolbar.right_action_items = right_actions

		left_actions = actions.get("left", [])
		toolbar.left_action_items = left_actions

	def render(self) -> MDTopAppBar:
		""" Render TopBar widget with a actions menu at left """

		toolbar = MDTopAppBar(
			title=self.title, opposite_colors=True,
			md_bg_color=(1, 1, 0, 1), type_height="small", elevation=4
		)

		self.widget = toolbar
		self.restore_toolbar()

		return toolbar


class ListMotorComponent(IComponent):
	""" ListMotorComponent class """

	id = "list_motor"

	def __init__(self, motors: Optional[List[dict]] = None):
		""" Instance list motor component
		:param motors: All motors to list
		"""
		super().__init__()
		self.motors = motors

	def refresh_data(self, motors: List[dict]) -> NoReturn:
		""" Refresh all motors in the list"""

		self.motors = motors

		layout = self.widget
		layout.clear_widgets()

		if motors:
			content = MDList()
			for motor in motors:
				content.add_widget(MotorItemComponent.build(motor))
		else:
			content = MDLabel(
				text="No Motors", halign="center", theme_text_color="Hint")

		layout.add_widget(content)

	def render(self) -> MDLabel | MDScrollView:
		""" Render motor results """
		self.widget = layout = MDScrollView()
		self.refresh_data(self.motors)
		return layout


class MotorFormComponent(IComponent):
	""" MotorFormComponent class """

	id = "motor_form"
	_filter_motor_view_model = Provide["filter_motor_view_model"]

	def _on_press_cancel_button(self, *args) -> NoReturn:
		""" Dismiss Form Dialog """
		self.dismiss()

	def _get_motor_inputs(self) -> dict:
		""" Get input values in the form """

		motor_inputs = {}
		for field in ("motor_type", "voltage", "kw", "rpm", "eff", "pf"):
			widget = self.content_cls.ids.get(field)
			motor_inputs[field] = widget.text

		return motor_inputs

	def _on_press_filter_button(self, *args) -> NoReturn:
		""" handle filter motor actions  """

		self.dismiss()
		self._filter_motor_view_model.execute(self._get_motor_inputs())

	def render(self) -> MDDialog:
		""" Render Motor Form Dialog """

		content = self.builder.load_file("fmotor/ui/widgets/forms.kv")

		cancel_button = MDFlatButton(
			text="CANCEL", theme_text_color="Custom",
			on_press=self._on_press_cancel_button)

		filter_button = MDFlatButton(
			text="Filter", theme_text_color="Custom",
			on_press=self._on_press_filter_button)

		dialog = MDDialog(
			size_hint=[0.9, None],
			title="Motor Data",
			type="custom",
			content_cls=content,
			buttons=[cancel_button, filter_button]
		)

		return dialog


class MotorComponent(IComponent):
	""" MotorComponent class """

	id = "motor"
	_estimate_motor_view_model = Provide["estimate_motor_view_model"]

	def __init__(self, motor=None):
		super().__init__()
		self.motor = motor or {}

	def refresh_data(self, motor: Optional[dict] = None) -> NoReturn:
		""" Refresh Motor Values """

		motor = prepare_motor_values(motor or {})

		motor_label_text = {
			"model": "[b]Model:[/b] %s " % motor.get("model"),
			"manufacturer": "[b]Manufacturer:[/b] %s" % motor.get("manufacturer"),
			"design": "[b]Design:[/b] %s" % motor.get("design"),
			"catalog": "[b]Catalog:[/b] %s" % motor.get("catalog"),
			"frame": "[b]Frame:[/b] %s" % motor.get("frame"),
			"voltage": "[b]Voltage:[/b] %s V" % motor.get("voltage"),
			"kw": "[b]Power:[/b] %s kw" % motor.get("kw"),
			"rpm": "[b]Speed:[/b] %s rpm" % motor.get("rpm")
		}

		for label_id, text in motor_label_text.items():
			label = self.widget.content_cls.ids.get(label_id)
			label.text = text

		datatable = self.widget.content_cls.ids.get("datatable")
		datatable.update_motor(motor)

		self.motor = motor

	def estimate(self, *args) -> NoReturn:
		""" Handle Estimate action """
		self.dismiss()
		self._estimate_motor_view_model.execute(self.motor)

	def calculate(self, **args) -> NoReturn:
		""" Handle calculate action """
		self.dismiss()

	def render(self):
		""" Render Motor Values in a Dialog """

		datatable = MotorDataTableComponent.build(self.motor)

		content = self.builder.load_file("fmotor/ui/widgets/motor.kv")
		content.add_widget(datatable)
		content.ids["datatable"] = datatable

		self.widget = dialog = MDDialog(
			title="Motor", type="custom", size_hint=[0.9, None],
			content_cls=content,
			buttons=[
				MDIconButton(
					icon="text-box-search-outline",
					on_press=self.estimate
				),
				MDIconButton(
					icon="calculator",
					on_press=self.calculate
				),
			]
		)

		return dialog


class MotorDataTableComponent(IComponent):
	""" MotorDataTableComponent class """

	_column_data = [
		("Kc", dp(20)),
		("100%", dp(20)),
		("75%", dp(20)),
		("50%", dp(20)),
		("25%", dp(20)),
	]

	def __init__(self, motor, **kwargs):
		super().__init__(**kwargs)
		self.motor = motor

	def update_motor(self, motor: Optional[dict] = None) -> NoReturn:
		""" Update rows from motor """

		motor = motor or {}

		new_data = self._get_table_data(motor)
		datatable = self.widget

		datatable.update_row(datatable.row_data[0], new_data[0])
		datatable.update_row(datatable.row_data[1], new_data[1])

	def _get_table_data(self, motor: Optional[dict] = None) -> NoReturn:
		""" Get rows from motor values """

		if not motor:
			motor = self.motor

		eff_row, pf_row = ["Eff"], ["PF"]

		for load in ("fl", "75", "50", "25"):
			eff_col = "eff_%s" % load
			eff_row.append(motor.get(eff_col, ""))

			pf_col = "pf_%s" % load
			pf_row.append(motor.get(pf_col, ""))

		return eff_row, pf_row

	def render(self) -> MDDataTable:
		""" Render Efficiency and power factor table of a given motor """

		datatable = MDDataTable(
			column_data=self._column_data,
			row_data=self._get_table_data()
		)
		return datatable


class EstimateMotorComponent(IComponent):
	""" EstimateMotorComponent class """

	id = "estimate_motor"

	def __init__(self, motor=None):
		super().__init__()
		self.motor = motor or {}

	def refresh_data(self, motor: dict) -> NoReturn:
		""" Refresh motor values """

		content = self.widget.content_cls
		motor = prepare_motor_values(motor)
		motor_label_text = {
			"voltage": "[b]Voltage:[/b] %s V" % motor.get("voltage"),
			"kw": "[b]Power:[/b] %s kw" % motor.get("kw"),
			"rpm": "[b]Speed:[/b] %s rpm" % motor.get("rpm")
		}

		for label_id, text in motor_label_text.items():
			label = content.ids.get(label_id)
			label.text = text

		datatable = content.ids.get("datatable")
		datatable.update_motor(motor)

		self.motor = motor

	def render(self) -> MDDialog:
		""" Render Dialog with Estimated motor values """

		content = self.builder.load_file("fmotor/ui/widgets/estimate.kv")

		datatable = MotorDataTableComponent.build(self.motor)
		content.add_widget(datatable)
		content.ids["datatable"] = datatable

		self.widget = dialog = MDDialog(title="Estimated Motor", type="custom",
		                                size_hint=[0.9, None], content_cls=content)

		return dialog
