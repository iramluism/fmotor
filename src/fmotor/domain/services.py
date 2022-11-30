""" Fmotor Domain Services Module """

from typing import List
from dependency_injector.wiring import Provide

from src.seedwork.domain.services import IService
from .entities import MotorEntity, MotorMeasurement
from .mappers import EstimateMotorMapper
from .utils import linear_interpolation, calculate_three_phase_current
from .aggregates import MotorAggregate


class GetNearestMotorService(IService):
	""" GetNearestMotorService class """

	_motor_validator = Provide["motor_validator"]
	_get_motor_error_service = Provide["get_motor_error_service"]

	def execute(self, motor_ref: MotorAggregate, motors: list[MotorAggregate]
	            ) -> List[MotorAggregate]:
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

		p_nom = None
		if motor.kw:
			p_nom = motor.kw * 1000
		elif motor.hp_nom:
			p_nom = motor.hp_nom / 1.341 * 1000

		if motor.v_nom and p_nom:
			if motor.eff_fl and motor.pf_fl:
				motor.i_fl = calculate_three_phase_current(
					p_nom, motor.v_nom, motor.eff_fl / 100, motor.pf_fl / 100
				)
			if motor.eff_75 and motor.pf_75:
				motor.i_75 = 0.75 * calculate_three_phase_current(
					p_nom, motor.v_nom, motor.eff_75 / 100, motor.pf_75 / 100
				)
			if motor.eff_50 and motor.pf_50:
				motor.i_50 = 0.5 * calculate_three_phase_current(
					p_nom, motor.v_nom, motor.eff_50 / 100, motor.pf_50 / 100
				)
			if motor.eff_25 and motor.pf_25:
				motor.i_25 = 0.25 * calculate_three_phase_current(
					p_nom, motor.v_nom, motor.eff_25 / 100, motor.pf_25 / 100
				)

		if motor.i_idle and motor.i_fl:
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

		p_nom = None
		if motor.kw:
			p_nom = motor.kw
		elif motor.hp_nom:
			p_nom = motor.hp_nom / 1.341

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

		if measurement_x.kc and p_nom:
			measurement_x.p_out = measurement_x.kc * p_nom

		if measurement_x.p_out and measurement_x.eff:
			measurement_x.p_in = measurement_x.p_out / measurement_x.eff

		if measurement_x.p_in and measurement_x.p_out:
			measurement_x.lost = measurement_x.p_in - measurement_x.p_out

		return measurement_x
