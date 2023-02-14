""" Fmotor Domain Validation Module """

from seedwork.domain.validations import IValidator
from .entities import MotorMeasurement
from .aggregates import MotorAggregate


class MotorValidator(IValidator):
	""" MotorValidator class """

	def execute(self, motor: MotorAggregate, raise_error=True):
		""" Validate motor entity fields """

		if not motor.p_nom:
			self.add_error("no declared Power")

		if raise_error and not self.is_valid():
			self.raise_errors()


class InterpolateMotorValidator(IValidator):

	def execute(self, measurement: MotorMeasurement, raise_error=True):

		motor = measurement.motor

		if measurement.current < motor.i_0:
			self.add_error("the current should be greater than load at 0 %")

		if measurement.current > motor.i_fl:
			self.add_error("the Current greater than nominal")

		if raise_error and not self.is_valid():
			self.raise_errors()
