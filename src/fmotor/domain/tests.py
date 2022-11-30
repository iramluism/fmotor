import unittest

from unittest.mock import MagicMock, Mock

from .services import (
	InterpolateMotorService,
	GetNearestMotorService,
	EstimateMotorService,
	GetMotorErrorService
)

from .validations import MotorValidator, InterpolateMotorValidator
from .entities import MotorEntity, MotorMeasurement
from .aggregates import MotorAggregate


class GetNearestMotorTestCase(unittest.TestCase):

	def setUp(self) -> None:
		error_service = GetMotorErrorService()
		GetNearestMotorService._get_motor_error_service = error_service
		GetNearestMotorService._motor_validator = Mock(execute=MagicMock())
		self.service = GetNearestMotorService()

		self.motors = [
			MotorAggregate(v_nom=110, kw=1.5, rpm=1800, pf_fl=1, pf_75=.85,
			               pf_50=0.86, pf_25=0.2, eff_75=0.71, eff_fl=.55),
			MotorAggregate(v_nom=110, kw=1.8, rpm=1600, pf_fl=.9, pf_75=.75,
			               pf_50=0.89, pf_25=0.85, eff_75=0.78, eff_fl=.28),
			MotorAggregate(v_nom=220, kw=1.8, rpm=1800, pf_fl=.58, pf_75=.75,
			               pf_50=0.59, pf_25=0.95, eff_75=0.95, eff_fl=.55),
		]

		self.motor = MotorAggregate(v_nom=220, kw=1.5, rpm=1800, pf_fl=.58,
		                            pf_75=.75, pf_50=0.59, pf_25=0.95,
		                            eff_75=0.95,
		                            eff_fl=.55)

		self._service = GetNearestMotorService()

	def test_order_by_error(self):
		nearest_motors = self.service.execute(self.motor, self.motors)

		errors = [motor.error for motor in nearest_motors]

		sorted_errors = sorted(errors)

		self.assertEqual(errors, sorted_errors)

	def test_not_find_motors(self):
		motor = MotorAggregate(v_nom=440, kw=4.5, rpm=900, pf_fl=.58,
		                       pf_75=.75, pf_50=0.59, pf_25=0.95, eff_75=0.95,
		                       eff_fl=.55)

		motors = self.service.execute(motor, self.motors)

		self.assertEqual(len(motors), 0)

	def test_error_margin(self):
		motors = self.service.execute(self.motor, self.motors)
		for motor in motors:
			self.assertLessEqual(motor.get("error"), 0.1)

	def test_validate_power(self):
		motor_without_kw = MotorAggregate(hp_nom=1)
		motor_without_hp = MotorAggregate(kw=1.2)
		motor_without_power = MotorAggregate()

		validator = MotorValidator()

		validator.clear_context()
		validator.execute(motor_without_kw, raise_error=False)
		self.assertTrue(validator.is_valid())

		validator.clear_context()
		validator.execute(motor_without_hp, raise_error=False)
		self.assertTrue(validator.is_valid())

		validator.clear_context()
		validator.execute(motor_without_power, raise_error=False)
		self.assertFalse(validator.is_valid())


class EstimateMotorTestCase(unittest.TestCase):

	def setUp(self) -> None:
		self.service = EstimateMotorService()

	def test_estimate_efficiency(self):

		motor_eval = MotorAggregate(
			v_nom=440, rpm=900, kw=1.1, pf_fl=.58, pf_75=.75, pf_50=0.59,
			pf_25=0.95
		)

		motor_ref = MotorAggregate(
			v_nom=440, rpm=900, kw=1.2, pf_fl=.58, pf_75=.75, pf_50=0.59,
			pf_25=0.95, eff_75=0.95, eff_fl=.55, eff_50=0.8, eff_25=0.9
		)

		motor = self.service.execute(motor_eval, motor_ref)

		self.assertEqual(motor.eff_fl, motor_ref.eff_fl)
		self.assertEqual(motor.eff_75, motor_ref.eff_75)
		self.assertEqual(motor.eff_50, motor_ref.eff_50)
		self.assertEqual(motor.eff_25, motor_ref.eff_25)

	def test_estimate_power_factor(self):

		motor_eval = MotorAggregate(v_nom=440, rpm=900, kw=1.1)

		motor_ref = MotorAggregate(v_nom=440, rpm=900, kw=1.2, pf_fl=.58,
		                           pf_75=.75, pf_50=0.59, pf_25=0.9)

		motor = self.service.execute(motor_eval, motor_ref)

		self.assertEqual(motor.pf_fl, motor_ref.pf_fl)
		self.assertEqual(motor.pf_75, motor_ref.pf_75)
		self.assertEqual(motor.pf_50, motor_ref.pf_50)
		self.assertEqual(motor.pf_25, motor_ref.pf_25)

	def test_estimate_current(self):

		motor_eval = MotorAggregate(v_nom=110, rpm=900, kw=1.1)
		motor_ref = MotorAggregate(
			pf_fl=71, pf_75=63, pf_50=52, pf_25=37,
			eff_fl=80.5, eff_75=82.5, eff_50=80.800, eff_25=74.19
		)

		motor = self.service.execute(motor_eval, motor_ref)

		self.assertAlmostEqual(motor.i_fl, 10.10, 1)
		self.assertAlmostEqual(motor.i_75, 8.33, 1)
		self.assertAlmostEqual(motor.i_50, 6.87, 1)
		self.assertAlmostEqual(motor.i_25, 5.25, 1)

	def test_priority_of_the_efficiency_and_power_factor_motor(self):

		motor_eval = MotorAggregate(v_nom=110, rpm=900, kw=1.1,
		                            eff_fl=98.2, pf_fl=90.1)

		motor_ref = MotorAggregate(
			v_nom=208, rpm=900, kw=1.32, pf_fl=71, pf_75=63, pf_50=52,
			pf_25=37, eff_fl=80.5, eff_75=82.5, eff_50=80.800, eff_25=74.19
		)

		motor = self.service.execute(motor_eval, motor_ref)

		self.assertEqual(motor.eff_fl, motor_eval.eff_fl)
		self.assertEqual(motor.pf_fl, motor_eval.pf_fl)


class InterpolateMotorValueTestCase(unittest.TestCase):

	def setUp(self) -> None:
		self.service = InterpolateMotorService()
		self.service._interpolate_motor_validation = Mock(
			execute=MagicMock())

	def test_interpolate_efficiency(self):
		motor = MotorEntity(
			eff_fl=68,
			eff_75=67.4,
			eff_50=63.4,
			eff_25=51,
			i_fl=80,
			i_75=50
		)

		measurement = MotorMeasurement(motor=motor, current=70)

		result = self.service.execute(measurement)
		self.assertLessEqual(result.eff, 68)
		self.assertGreaterEqual(result.eff, 67)
		self.assertEqual(result.current, 70)

		measurement = MotorMeasurement(motor=motor, current=50)
		result = self.service.execute(measurement)
		self.assertAlmostEqual(result.eff, 67.4, 0)

	def test_interpolate_efficiency_with_missing_currents(self):
		motor = MotorEntity(
			eff_fl=68,
			eff_75=67.4,
			eff_50=63.4,
			eff_25=51,
			i_fl=80,
			i_75=50
		)

		measurement = MotorMeasurement(motor=motor, current=40)
		result = self.service.execute(measurement)
		self.assertLessEqual(result.eff, 67.4)
		self.assertGreaterEqual(result.eff, 63.4)
		self.assertEqual(result.current, 40)

	def test_raise_error_when_current_is_greater_than_nominal(self):

		motor = MotorEntity(i_fl=5)

		validator = InterpolateMotorValidator()

		measurement = MotorMeasurement(motor, current=8)
		validator.execute(measurement, raise_error=False)
		self.assertFalse(validator.is_valid())

	def test_just_calculate_for_current_less_equal_than_nominal(self):
		motor = MotorEntity(i_fl=5)

		validator = InterpolateMotorValidator()

		measurement = MotorMeasurement(motor, current=3.2)

		validator.clear_context()
		validator.execute(measurement, raise_error=False)
		self.assertTrue(validator.is_valid())

		validator.clear_context()
		measurement = MotorMeasurement(motor, current=5)
		validator.execute(measurement, raise_error=False)
		self.assertTrue(validator.is_valid())


if __name__ == '__main__':
	unittest.main()
