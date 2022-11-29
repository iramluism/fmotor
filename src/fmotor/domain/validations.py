""" Fmotor Domain Validation Module """

from src.seedwork.domain.validations import IValidator
from .entities import MotorEntity, MotorMeasurement


class MotorValidator(IValidator):
	""" MotorValidator class """

	def execute(self, motor: MotorEntity, raise_error=True):
		""" Validate motor entity fields """

		if not motor.hp_nom:
			self.add_error("no declared Power")

		if raise_error and not self.is_valid():
			self.raise_errors()


class InterpolateMotorValidator(IValidator):

	def execute(self, measurement: MotorMeasurement, raise_error=True):

		motor = measurement.motor

		if measurement.current > motor.i_fl:
			self.add_error("the Current greater than nominal")

		if raise_error and not self.is_valid():
			self.raise_errors()
