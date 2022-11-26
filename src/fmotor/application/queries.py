""" Fmotor Application Queries Module """

from dependency_injector.wiring import Provide

from src.seedwork.application.queries import IQuery
from src.fmotor.application.mappers import MotorMapper
from .dtos import FilterMotorQueryDTO, MotorDTO


class FilterMotorQuery(IQuery):
	""" FilterMotorQuery class """

	_motor_repository = Provide["motor_repository"]
	_get_nearest_motor_service = Provide["get_nearest_motor_service"]

	def execute(self, motor_ref: MotorDTO) -> FilterMotorQueryDTO:
		""" Find the nearest motors
		:param motor_ref: Reference Motor
		"""

		if motor_ref.motor_type:
			motors = self._motor_repository.filters(
				motor_type=motor_ref.motor_type)
		else:
			motors = self._motor_repository.all()

		motor_ref = MotorMapper.create_entity(motor_ref)

		closest_motors = self._get_nearest_motor_service.execute(motor_ref, motors)

		filter_motor_dto = FilterMotorQueryDTO()
		for motor in closest_motors:
			motor_dto = MotorMapper.create_dto(motor)
			filter_motor_dto.motors.append(motor_dto)

		return filter_motor_dto
