""" Fmotor UI Events Module """

from typing import Optional, List, NoReturn

from src.seedwork.ui.events import IEvent
from src.seedwork.ui.utils import get_component


class MotorListEvent(IEvent):
	""" MotorListEvent class """

	def handle(self, motors: Optional[List[dict]] = None) -> NoReturn:
		""" refresh motors in the list component """

		list_motor_component = get_component("list_motor")
		list_motor_component.refresh_data(motors)


class EstimateMotorEvent(IEvent):
	""" EstimateMotorEvent class """

	def handle(self, motor: dict) -> NoReturn:
		""" Show estimation motor dialog """

		motor_dialog_component = get_component("estimate_motor")
		motor_dialog_component.refresh_data(motor)
		motor_dialog_component.open()
