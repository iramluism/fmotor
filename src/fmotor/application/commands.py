""" Fmotor Application Commands Module """

import inject

from seedwork.application.commands import ICommand

from fmotor.application.mappers import MotorMapper, MotorMeasurementMapper

from fmotor.application.dtos import (
	EstimateMotorDTI,
	MotorDTO,
	CalculateMotorDTO
)

from fmotor.domain.services import InterpolateMotorService
from fmotor.domain.services import EstimateMotorService
from fmotor.infrastructure.repositories import MotorRepository


class CalculateMotorCommand(ICommand):
	""" CalculateMotorCommand class """

	_calculate_motor_service = inject.attr(InterpolateMotorService)

	def execute(self, calculate_motor_dti: CalculateMotorDTO
	            ) -> CalculateMotorDTO:
		""" Calculate Motor values for a given load """

		measurement = MotorMeasurementMapper.create_entity(calculate_motor_dti)

		motor_values = self._calculate_motor_service.execute(measurement)

		motor_values_dto = MotorMeasurementMapper.create_dto(motor_values)

		return motor_values_dto


class EstimateMotorCommand(ICommand):
	""" EstimateMotorCommand class """

	_estimate_motor_service = inject.attr(EstimateMotorService)
	_motor_repository = inject.attr(MotorRepository)

	def execute(self, estimate_motor_dti: EstimateMotorDTI) -> MotorDTO:
		""" Compare two motors to estimate values """

		motor_eval = MotorMapper.create_aggregate(estimate_motor_dti.motor_eval)
		motor_ref = MotorMapper.create_aggregate(estimate_motor_dti.motor_ref)

		estimated_motor = self._estimate_motor_service.execute(motor_eval, motor_ref)

		estimated_motor_dto = MotorMapper.create_dto(estimated_motor)

		return estimated_motor_dto
