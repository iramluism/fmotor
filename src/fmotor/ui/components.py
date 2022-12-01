""" Fmotor UI Components Module """

from typing import List, Optional, NoReturn

from dependency_injector.wiring import Provide
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, IconLeftWidget, OneLineAvatarListItem
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (
	MDFlatButton,
	MDFloatingActionButton,
	MDIconButton, MDRaisedButton
)

from kivymd.uix.spinner import MDSpinner

from fmotor.ui.utils import prepare_motor_values
from seedwork.ui.utils import _
from seedwork.ui.components import IComponent


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
		ErrorDialogComponent.build()

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

	def set_spinner_component(self):
		spinner = MDScreen(
			MDSpinner(
				size_hint=(None, None),
				size=(dp(46), dp(46)),
				pos_hint={'center_x': .5, 'center_y': .5}
			),
			MDLabel(
				text=_("Finding nearest motors ..."),
				halign="center",
				theme_text_color="Hint",
				font_style="Caption",
				pos_hint={'center_x': .5, 'center_y': .4}
			),
		)
		layout = self.widget
		layout.clear_widgets()
		layout.add_widget(spinner)

	def refresh_data(self, motors: Optional[List[dict]] = None) -> NoReturn:
		""" Refresh all motors in the list"""

		self.motors = motors or []

		layout = self.widget
		layout.clear_widgets()

		if motors:
			content = MDList()
			for motor in motors:
				content.add_widget(MotorItemComponent.build(motor))
		else:

			content = MDScreen()

			content.add_widget(
				MDLabel(text=_("No Motors"), halign="center",
				        theme_text_color="Hint", font_style="Body1")
			)

			content.add_widget(
				MDLabel(text=_("Tap the Search button to find motors"),
				        halign="center", theme_text_color="Hint",
				        pos_hint={"center_y": 0.45}, font_style="Caption")
			)

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
	_motor_cache = Provide["motor_cache"]
	dialog = None

	@classmethod
	def _init_dialog(cls):
		content = cls.builder.load_file("fmotor/ui/widgets/forms.kv")

		cancel_button = MDFlatButton(
			text=_("CANCEL"), theme_text_color="Custom",
			on_press=lambda e: cls._on_press_cancel_button())

		filter_button = MDRaisedButton(
			text=_("FILTER"), theme_text_color="Custom", text_color="white",
			on_press=lambda e: cls._on_press_filter_button())

		dialog = MDDialog(
			size_hint=[0.9, None],
			title=_("Motor Data"),
			type="custom",
			content_cls=content,
			buttons=[cancel_button, filter_button]
		)

		return dialog

	@classmethod
	def render_dialog(cls):
		if not cls.dialog:
			cls.dialog = cls._init_dialog()
		return cls.dialog

	@classmethod
	def _on_press_cancel_button(cls) -> NoReturn:
		""" Dismiss Form Dialog """
		cls.dialog.dismiss()

	@classmethod
	def _on_press_filter_button(cls) -> NoReturn:
		""" handle filter motor actions  """

		cls.dialog.dismiss()

		motor_inputs = {}
		for field in ("voltage", "kw", "rpm", "eff", "pf"):
			widget = cls.dialog.content_cls.ids.get(field)
			if widget.text:
				motor_inputs[field] = widget.text

		cls._filter_motor_view_model.execute(motor_inputs)

	def render(self) -> MDDialog:
		""" Render Motor Form Dialog """
		dialog = self.render_dialog()
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

		motor_label_text = [
			("model", "[b]%s:[/b] %s ", _("Model"), motor.get("model")),
			("manufacturer", "[b]%s:[/b] %s", _("Manufacturer"), motor.get("manufacturer")),
			("design", "[b]%s:[/b] %s" , _("Design"), motor.get("design")),
			("catalog", "[b]%s:[/b] %s", _("Catalog"), motor.get("catalog")),
			("frame", "[b]%s:[/b] %s", _("Frame"), motor.get("frame")),
			("voltage", "[b]%s:[/b] %s V", _("Voltage"), motor.get("voltage")),
			("kw", "[b]%s:[/b] %s kw", _("Power"), motor.get("kw")),
			("rpm", "[b]%s:[/b] %s", _("rpm"), motor.get("rpm"))
		]

		for label_id, label_template, label_name, value, in motor_label_text:
			label = self.widget.content_cls.ids.get(label_id)
			label.text = label_template % (label_name, value)

		datatable = self.widget.content_cls.ids.get("datatable")
		datatable.update_motor(motor)

		self.motor = motor

	def estimate(self) -> NoReturn:
		""" Handle Estimate action """
		self.dismiss()
		self._estimate_motor_view_model.execute(self.motor)

	def calculate(self) -> NoReturn:
		""" Handle calculate action """
		self.dismiss()
		form = CalculateFormComponent.build(self.motor)
		form.open()

	def render(self):
		""" Render Motor Values in a Dialog """

		datatable = MotorDataTableComponent.build(self.motor)

		content = self.builder.load_file("fmotor/ui/widgets/motor.kv")
		content.add_widget(datatable)
		content.ids["datatable"] = datatable

		self.widget = dialog = MDDialog(
			title=_("Motor"), type="custom", size_hint=[0.9, None],
			content_cls=content,
			buttons=[
				MDIconButton(
					icon="text-box-search-outline",
					on_press=lambda e: self.estimate()
				),
				MDIconButton(
					icon="calculator",
					on_press=lambda e: self.calculate()
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
		datatable.update_row(datatable.row_data[2], new_data[2])

	def _get_table_data(self, motor: Optional[dict] = None) -> NoReturn:
		""" Get rows from motor values """

		if not motor:
			motor = self.motor

		eff_row, pf_row, amps_row = [_("eff")], [_("pf")], [_("amps")]

		for load in ("fl", "75", "50", "25"):
			eff = motor.get("eff_%s" % load)
			eff_row.append(eff or "")

			pf = motor.get("pf_%s" % load)
			pf_row.append(pf or "")

			amps = motor.get("i_%s" % load)
			amps_row.append(amps or "")

		return eff_row, pf_row, amps_row

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
			"voltage": "[b]%s:[/b] %s V" % (_("Voltage"), motor.get("v_nom")),
			"kw": "[b]%s:[/b] %s kw" % (_("Power"), motor.get("kw")),
			"rpm": "[b]rpm:[/b] %s rpm" % motor.get("rpm")
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

		self.widget = dialog = MDDialog(title=_("Estimation"), type="custom",
		                                size_hint=[0.9, None],
		                                content_cls=content)

		return dialog


class CalculateFormComponent(IComponent):
	id = "calculate_form"

	_calculate_motor_view_model = Provide["calculate_motor_view_model"]

	def __init__(self, motor):
		super().__init__()
		self.motor = motor

	def refresh_data(self, motor):
		layout = self.content_cls
		content = layout.ids.get("content")

		motor = prepare_motor_values(motor)

		label_args = {
			"markup": True,
			"halign": "center",
			"theme_text_color": "Hint",
		}

		content.clear_widgets()

		content.add_widget(
			MDGridLayout(
				MDLabel(text="[b]%s:[/b] %s " % (_("Load Factor"), motor.get("kc")),
				        **label_args),
				MDLabel(text="[b]%s:[/b] %s " % (_("Power Factor"), motor.get("pf")),
				        **label_args),
				MDLabel(text="[b]%s:[/b] %s " % (_("Efficiency"), motor.get("eff")),
				        **label_args),
				MDLabel(text="[b]%s:[/b] %s kw" % (_("Power Out"), motor.get("p_out")),
				        **label_args),
				MDLabel(text="[b]%s:[/b] %s kw" % (_("Power In"), motor.get("p_in")),
				        **label_args),
				MDLabel(text="[b]%s:[/b] %s kw" % (_("Losses"), motor.get("losses")),
				        **label_args),
				cols=2,
			)
		)

	def calculate(self):
		layout = self.content_cls
		current = layout.ids.get("current")
		self._calculate_motor_view_model.execute(self.motor, current.text)

	def render(self):
		content = self.builder.load_file("fmotor/ui/widgets/calculate.kv")

		self.widget = dialog = MDDialog(
			title=_("Calculate Motor"), type="custom",
			size_hint=[0.9, None],
			content_cls=content,
			buttons=[
				MDFlatButton(
					text=_("CANCEL"), theme_text_color="Custom",
					on_press=lambda e: self.dismiss()
				),
				MDRaisedButton(
					text=_("CALCULATE"), theme_text_color="Custom",
					text_color="white",
					on_press=lambda e: self.calculate()
				)
			]
		)

		return dialog


class ErrorDialogComponent(IComponent):
	id = "error_dialog"

	def __init__(self, errors: Optional[list] = None):
		super().__init__()
		self.errors = errors or []

	def add_errors(self, errors):
		self.errors = errors
		dialog = self.widget

		items = [OneLineAvatarListItem(text=error) for error in self.errors]
		dialog.update_items(items)

	def render(self):
		dialog = MDDialog(title=_("Error"), type="custom",
		                  size_hint=[0.9, None])

		return dialog
