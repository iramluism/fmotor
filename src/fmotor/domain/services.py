""" Fmotor Domain Services Module """

from typing import List
from dependency_injector.wiring import Provide

from src.seedwork.domain.services import IService
from .entities import MotorEntity
from .mappers import EstimateMotorMapper


class GetExactVoltageService(IService):
	""" GetExactVoltageService class """

from .aggregates import MotorAggregate


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

	def execute(self, motor_eval: MotorAggregate, motor_ref: MotorAggregate
	            ) -> MotorAggregate:
		""" Estimate motor values using two motors """

		motor = EstimateMotorMapper.create_motor(motor_eval, motor_ref)

		watts_nom = motor.kw * 1000

		motor.i_fl = 100 * watts_nom / (
				math.sqrt(3) * motor.v_nom * motor.eff_fl * motor.pf_fl)

		motor.i_75 = 75 * watts_nom / (
				math.sqrt(3) * motor.v_nom * motor.eff_75 * motor.pf_75)

		motor.i_50 = 50 * watts_nom / (
				math.sqrt(3) * motor.v_nom * motor.eff_50 * motor.pf_50)

		motor.i_25 = 25 * watts_nom / (
				math.sqrt(3) * motor.v_nom * motor.eff_25 * motor.pf_25)

		ki0 = motor.i_idle / motor.i_fl

		motor.i_0 = motor.i_fl * ki0

		return motor
