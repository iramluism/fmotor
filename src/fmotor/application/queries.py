""" Fmotor Application Queries Module """

import inject

from seedwork.application.queries import IQuery
from fmotor.application.mappers import MotorMapper
from fmotor.domain.services import GetNearestMotorService
from fmotor.infrastructure.repositories import MotorRepository

from .dtos import FilterMotorQueryDTO, MotorDTO


class FilterMotorQuery(IQuery):
	""" FilterMotorQuery class """

	_motor_repository = inject.attr(MotorRepository)
	_get_nearest_motor_service = inject.attr(GetNearestMotorService)

	def execute(self, motor_ref: MotorDTO) -> FilterMotorQueryDTO:
		""" Find the nearest motors
		:param motor_ref: Reference Motor
		"""

		filters = {}
		if motor_ref.v_nom:
			filters["v_nom"] = motor_ref.v_nom

		motors = self._motor_repository.filter(**filters)

		motor_ref = MotorMapper.create_aggregate(motor_ref)

		closest_motors = \
			self._get_nearest_motor_service.execute(motor_ref, motors)

		filter_motor_dto = FilterMotorQueryDTO()
		for motor in closest_motors[:30]:
			motor_dto = MotorMapper.create_dto(motor)
			filter_motor_dto.motors.append(motor_dto)

		return filter_motor_dto
