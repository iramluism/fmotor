""" Fmotor Domain Services Module """

import math

from typing import List
from dependency_injector.wiring import Provide

from src.seedwork.domain.services import IService
from .entities import MotorEntity, MotorMeasurement
from .mappers import EstimateMotorMapper
from .utils import linear_interpolation
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
		for field in ("kw", "rpm", "eff_fl", "pf_fl"):
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


class InterpolateMotorService(IService):
	""" InterpolateMotorService """

	_interpolate_motor_validation = Provide["interpolate_motor_validator"]

	def execute(self, measurement: MotorMeasurement) -> MotorMeasurement:
		""" Calculate power out, power factor, power in, lost and efficiency
		for a given load connected to a motor.
		:param measurement: motor measurement, when current and motor are mandatory
		"""

		self._interpolate_motor_validation.execute(measurement)

		motor = measurement.motor

		i_ranges = [
			(.25, motor.i_25, motor.eff_25, motor.pf_25),
			(.5, motor.i_50, motor.eff_50, motor.pf_50),
			(.75, motor.i_75, motor.eff_75, motor.pf_75),
			(1, motor.i_fl, motor.eff_fl, motor.pf_fl)
		]

		i_x = measurement.current

		idx_up = None
		for idx, current in enumerate(i_ranges):
			i = current[1]
			if i and i_x <= i:
				idx_up = idx

		measurement_x = MotorMeasurement(motor=motor, current=i_x)

		kc_up, i_up, eff_up, pf_up = i_ranges[idx_up]
		kc_down, i_down, eff_down, pf_down = i_ranges[idx_up - 1]
		if kc_up and kc_down:
			measurement_x.kc = linear_interpolation(
				(i_down, kc_down), (i_up, kc_up), i_x)

		if eff_up and eff_down:
			measurement_x.eff = linear_interpolation(
				(i_down, eff_down), (i_up, eff_up), i_x)

		if pf_up and pf_down:
			measurement_x.pf = linear_interpolation(
				(i_down, pf_down), (i_up, pf_up), i_x)

		if measurement_x.kc:
			measurement_x.p_out = measurement_x.kc * motor.hp_nom / 1.341

		if measurement_x.p_out and measurement_x.eff:
			measurement_x.p_in = measurement_x.p_out / measurement_x.eff

		if measurement_x.p_in and measurement_x.p_out:
			measurement_x.lost = measurement_x.p_in - measurement_x.p_out

		return measurement_x
