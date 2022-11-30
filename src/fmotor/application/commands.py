""" Fmotor Application Commands Module """

from dependency_injector.wiring import Provide

from src.seedwork.application.commands import ICommand

from src.fmotor.application.mappers import MotorMapper, MotorMeasurementMapper

from src.fmotor.application.dtos import (
	EstimateMotorDTI,
	MotorDTO,
	CalculateMotorDTO
)


class CalculateMotorCommand(ICommand):
	""" CalculateMotorCommand class """

	_calculate_motor_service = Provide["interpolate_motor_service"]

	def execute(self, calculate_motor_dti: CalculateMotorDTO
	            ) -> CalculateMotorDTO:
		""" Calculate Motor values for a given load """

		measurement = MotorMeasurementMapper.create_entity(calculate_motor_dti)

		motor_values = self._calculate_motor_service.execute(measurement)

		motor_values_dto = MotorMeasurementMapper.create_dto(motor_values)

		return motor_values_dto


class EstimateMotorCommand(ICommand):
	""" EstimateMotorCommand class """

	_estimate_motor_service = Provide["estimate_motor_service"]
	_motor_repository = Provide["motor_repository"]

	def execute(self, estimate_motor_dti: EstimateMotorDTI) -> MotorDTO:
		""" Compare two motors to estimate values """

		motor_eval = MotorMapper.create_aggregate(estimate_motor_dti.motor_eval)
		motor_ref = MotorMapper.create_aggregate(estimate_motor_dti.motor_ref)

		estimated_motor = self._estimate_motor_service.execute(motor_eval, motor_ref)

		estimated_motor_dto = MotorMapper.create_dto(estimated_motor)

		return estimated_motor_dto
