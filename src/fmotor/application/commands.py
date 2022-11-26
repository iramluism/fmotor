""" Fmotor Application Commands Module """

from dependency_injector.wiring import Provide

from src.seedwork.application.commands import ICommand
from src.fmotor.application.mappers import MotorMapper
from src.fmotor.application.dtos import EstimateMotorDTI, MotorDTO


class EstimateMotorCommand(ICommand):
	""" EstimateMotorCommand class """

	_estimate_motor_service = Provide["estimate_motor_service"]
	_motor_repository = Provide["motor_repository"]

	def execute(self, estimate_motor_dti: EstimateMotorDTI) -> MotorDTO:
		""" Compare two motors to estimate values """

		motor_eval = MotorMapper.create_entity(estimate_motor_dti.motor_eval)
		motor_ref = MotorMapper.create_entity(estimate_motor_dti.motor_ref)

		estimated_motor = self._estimate_motor_service.execute(motor_eval, motor_ref)

		estimated_motor_dto = MotorMapper.create_dto(estimated_motor)

		return estimated_motor_dto
