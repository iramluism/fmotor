""" FMotor UI View Model Module """


import time
import threading


from dependency_injector.wiring import Provide
from src.seedwork.ui.view_models import IViewModel
from src.fmotor.application.dtos import MotorDTO, EstimateMotorDTI
from src.fmotor.ui.utils import convert

from .events import MotorListEvent, EstimateMotorEvent


class FilterMotorViewModel(IViewModel):
	""" FilterMotorViewModel class """

	_filter_motor_query = Provide["filter_motor_query"]
	_motor_cache = Provide["motor_cache"]

	def filter_motors(self, motor):

		FilterMotorEvent.dispatch()

		time.sleep(0.2)

		filter_motor_dto = self._filter_motor_query.execute(motor)

		self._motor_cache.set("cur_motor", motor.as_dict())

		motors = filter_motor_dto.as_dict().get("motors")

		MotorListEvent.dispatch(motors)

	def execute(self, motor: dict):
		""" Get motors from model """

		try:
			motor = MotorDTO(
				type=convert(motor.get("motor_type"), str),
				v_nom=convert(motor.get("voltage"), float),
				kw=convert(motor.get("kw"), float),
				rpm=convert(motor.get("rpm"), float),
				eff_fl=convert(motor.get("eff"), float),
				pf_fl=convert(motor.get("pf"), float)
			)

			thread = threading.Thread(
				target=self.filter_motors, args=[motor])
			thread.start()

		except Exception as e:
			raise e


class EstimateMotorViewModel(IViewModel):
	""" EstimateMotorViewModel class """

	_estimate_motor_command = Provide["estimate_motor_command"]
	_motor_cache = Provide["motor_cache"]

	def execute(self, motor):
		""" Get estimated motor from model """

		motor_eval = self._motor_cache.get("cur_motor")

		estimate_motor_dti = EstimateMotorDTI(
			motor_eval=motor_eval,
			motor_ref=motor
		)

		estimated_values = self._estimate_motor_command.execute(estimate_motor_dti)

		EstimateMotorEvent.execute(estimated_values)
