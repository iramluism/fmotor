""" Fmotor Domain Validation Module """

from src.seedwork.domain.validations import IValidator
from .entities import MotorEntity


class MotorValidator(IValidator):
	""" MotorValidator class """

	def execute(self, motor: MotorEntity, raise_error=True):
		""" Validate motor entity fields """

		if not motor.hp_nom:
			self.add_error("no declared Power")
		if not motor.v_nom:
			self.add_error("no declared Voltage")

		if raise_error and not self.is_valid():
			self.raise_errors()
