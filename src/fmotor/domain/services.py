""" Fmotor Domain Services Module """

from typing import List
from dependency_injector.wiring import Provide

from src.seedwork.domain.services import IService
from .entities import MotorEntity
from .mappers import EstimateMotorMapper


class GetExactVoltageService(IService):
	""" GetExactVoltageService class """

	def execute(self, voltage: float) -> int:
		""" Return Voltage Id from a given voltage """

		voltage_range = {
			200: [2],
			208: [4, 5],
			220: [11],
			230: [4, 5, 12],
			440: [11],
			460: [6, 7, 12, 13],
			575: [8],
			796: [12, 13],
			2300: [9, 14],
			4000: [10, 14, 15]
		}

		max_v = max(voltage_range, key=lambda v: v <= voltage)
		return min(voltage_range[max_v])


class GetNearestMotorService(IService):
	""" GetNearestMotorService class """

	_motor_validator = Provide["motor_validator"]
	_get_low_voltage_service = Provide["get_low_voltage_service"]
	_get_motor_error_service = Provide["get_motor_error_service"]

	def execute(self, motor_ref: MotorEntity, motors: list[MotorEntity]
	            ) -> List[MotorEntity]:
		""" Get Nearest Motor to a reference motor
		:param motor_ref: Reference motor
		:param motors: Motors to evaluate
		"""

		self._motor_validator.execute(motor_ref)

		likely_motors = []
		for motor in motors:
			error = self._get_motor_error_service.execute(motor, motor_ref)
			if error < 0.1:
				motor.error = error
				likely_motors.append(motor)

		sorted_motors = sorted(likely_motors, key=lambda m: m.error)

		return sorted_motors


class GetMotorErrorService(IService):
	""" GetMotorErrorService class """

	def execute(self, motor_eval: MotorEntity, motor_ref: MotorEntity) -> float:
		""" Calculate the error between two motors """

		error = 0
		for field in ("rpm", "eff_fl", "pf_fl"):
			error += (motor_eval.get(field) / motor_ref.get(field) - 1) ** 2

		return error


class EstimateMotorService(IService):
	""" EstimateMotorService class """

	def execute(self, motor_eval: MotorEntity, motor_ref: MotorEntity
	            ) -> MotorEntity:
		""" Estimate motor values using two motors """

		motor = EstimateMotorMapper.create_motor(motor_eval, motor_ref)
		return motor
