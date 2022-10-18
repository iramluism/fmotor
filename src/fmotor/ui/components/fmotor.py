""" Fmotor App Component Module """
from dependency_injector.wiring import Provide
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem

from src.seedwork.ui.components import IComponent
from src.fmotor.ui.components.search_button import FloatButtonComponent


from src.fmotor.ui.dtos import (
	FilterMotorViewModelDTI,
	EstimateMotorPropertiesViewModelDTI,
	CalculateMotorPropertiesViewModelDTI
)

from .forms import LoadDataTabComponent, MotorDataTabComponent, MotorControlFormComponent


class FMotorAppComponent(IComponent):
	""" FMotorAppComponent class """

	_get_motor_detail_view_model = Provide["get_motor_detail_view_model"]
	_filter_motor_view_model = Provide["filter_motor_view_model"]
	_calculate_motor_properties_view_model = \
		Provide["calculate_motor_properties_view_model"]
	_estimate_motor_properties_view_model = \
		Provide["estimate_motor_properties_view_model"]

	def open_similar_motors_dialog(self, *args):
		""" Show motors according to the filter """

		self._filter_motor_view_model.execute(
			FilterMotorViewModelDTI(catalog="sdfsdf", model="sdfsd"))

	def estimate_motor_properties(self):
		self._estimate_motor_properties_view_model.execute(
			EstimateMotorPropertiesViewModelDTI())

	def calculate_motor_properties(self):
		self._calculate_motor_properties_view_model.execute(
			CalculateMotorPropertiesViewModelDTI)

	def render(self):
		layout = MDFloatLayout()
		box_layout = MDBoxLayout(orientation="vertical")
		top_bar = MDTopAppBar(title="fMotor", opposite_colors=True,
		                      md_bg_color=(1, 1, 0, 1), type_height="small",
		                      elevation=4)

		box_layout.add_widget(top_bar)

		motor_form = MotorControlFormComponent.build()

		box_layout.add_widget(motor_form)

		layout.add_widget(box_layout)

		button = FloatButtonComponent.build(
			search_action=self.open_similar_motors_dialog,
			calculate_action=self.calculate_motor_properties,
			estimate_action=self.estimate_motor_properties
		)

		layout.add_widget(button)

		return layout
