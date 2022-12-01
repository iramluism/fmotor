""" FMotor UI View Model Module """


import time
import threading

from dependency_injector.wiring import Provide
from seedwork.ui.view_models import IViewModel
from fmotor.ui.utils import convert, parse_error_messages

from fmotor.application.dtos import (
	MotorDTO,
	EstimateMotorDTI,
	CalculateMotorDTO
)

from .events import (
	MotorListEvent,
	EstimateMotorEvent,
	FilterMotorEvent,
	CalculateMotorEvent,
	ErrorEvent,
	NoMotorEvent
)


class FilterMotorViewModel(IViewModel):
	""" FilterMotorViewModel class """

	_filter_motor_query = Provide["filter_motor_query"]
	_motor_cache = Provide["motor_cache"]

	def filter_motors(self, motor):

		FilterMotorEvent.dispatch()

		motor = MotorDTO(
			type=convert(motor.get("motor_type"), str),
			v_nom=convert(motor.get("voltage"), float),
			kw=convert(motor.get("kw"), float),
			rpm=convert(motor.get("rpm"), float),
			eff_fl=convert(motor.get("eff"), float, 100),
			pf_fl=convert(motor.get("pf"), float, 100)
		)

		time.sleep(0.2)

		try:

			filter_motor_dto = self._filter_motor_query.execute(motor)

		except Exception as e:
			raise e
		else:
			self._motor_cache.set("cur_motor", motor.as_dict())

			motors = filter_motor_dto.as_dict().get("motors")
			MotorListEvent.dispatch(motors)

	def execute(self, motor: dict):
		""" Get motors from model """

		if not motor:
			NoMotorEvent.dispatch()
		else:
			thread = threading.Thread(target=self.filter_motors, args=[motor])
			thread.start()


class EstimateMotorViewModel(IViewModel):
	""" EstimateMotorViewModel class """

	_estimate_motor_command = Provide["estimate_motor_command"]
	_motor_cache = Provide["motor_cache"]

	def estimate_motor(self, motor):
		motor_eval = self._motor_cache.get("cur_motor")

		estimate_motor_dti = EstimateMotorDTI(
			motor_eval=MotorDTO(**motor_eval),
			motor_ref=MotorDTO(**motor)
		)

		estimated_values = self._estimate_motor_command.execute(
			estimate_motor_dti)

		return estimated_values.as_dict()

	def execute(self, motor):
		""" Get estimated motor from model """

		estimated_values = self.estimate_motor(motor)
		EstimateMotorEvent.dispatch(estimated_values)


class CalculateMotorViewModel(IViewModel):

	_calculate_motor_command = Provide["calculate_motor_command"]
	_estimate_motor_command = Provide["estimate_motor_command"]
	_motor_cache = Provide["motor_cache"]

	def execute(self, motor: dict, current):

		motor_eval = self._motor_cache.get("cur_motor")

		try:

			estimate_motor_dti = EstimateMotorDTI(
				motor_eval=MotorDTO(**motor_eval),
				motor_ref=MotorDTO(**motor)
			)

			estimated_motor = \
				self._estimate_motor_command.execute(estimate_motor_dti)

			calculate_motor_dti = CalculateMotorDTO(
				motor=estimated_motor,
				current=convert(current, float)
			)

			calculated_motor = self._calculate_motor_command.execute(
				calculate_motor_dti)

		except Exception as e:
			messages = parse_error_messages(e)
			ErrorEvent.dispatch(messages)
		else:
			CalculateMotorEvent.dispatch(calculated_motor.as_dict())
