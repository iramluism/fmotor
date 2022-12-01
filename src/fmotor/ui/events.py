""" Fmotor UI Events Module """

from typing import Optional, List

from kivy.clock import mainthread, Clock

from src.seedwork.ui.events import IEvent
from src.seedwork.ui.utils import get_component


class MotorListEvent(IEvent):
	""" MotorListEvent class """

	@mainthread
	def handle(self, motors: Optional[List[dict]] = None):
		""" refresh motors in the list component """

		list_motor_component = get_component("list_motor")
		list_motor_component.refresh_data(motors)
		FilterMotorTimeOutEvent.cancel()


class EstimateMotorEvent(IEvent):
	""" EstimateMotorEvent class """

	@mainthread
	def handle(self, motor: dict):
		""" Show estimation motor dialog """

		motor_dialog_component = get_component("estimate_motor")
		motor_dialog_component.refresh_data(motor)
		motor_dialog_component.open()


class ErrorEvent(IEvent):
	""" ErrorEvent class """

	def handle(self, errors: Optional[list] = None):
		""" Show error dialog """

		component = get_component("error_dialog")
		component.add_errors(errors or [])
		component.open()


class FilterMotorEvent(IEvent):
	""" FilterMotorEvent class """

	@mainthread
	def handle(self):
		""" Add to list component a spinner """
		list_motor_component = get_component("list_motor")
		list_motor_component.set_spinner_component()
		FilterMotorTimeOutEvent.dispatch(timeout=90)


class CalculateMotorEvent(IEvent):
	""" CalculateMotorEvent class """

	@mainthread
	def handle(self, motor):
		""" Refresh Calculate form dialog with the calculated values """
		calculate_form = get_component("calculate_form")
		calculate_form.refresh_data(motor)


class FilterMotorTimeOutEvent(IEvent):
	""" FilterMotorTimeOutEvent class """

	@mainthread
	def handle(self):
		""" update list with no motors """
		list_motor_component = get_component("list_motor")
		list_motor_component.refresh_data()


class NoMotorEvent(IEvent):

	@mainthread
	def handle(self):
		""" update list with no motors """
		list_motor_component = get_component("list_motor")
		list_motor_component.refresh_data()
