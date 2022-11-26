""" Fmotor Application Mappers Module """

from src.seedwork.application.mappers import IMapper

from .dtos import MotorDTO
from src.fmotor.domain.entities import MotorEntity


class MotorMapper(IMapper):
	""" MotorMapper class """

	@classmethod
	def create_entity(cls, motor_dto: MotorDTO) -> MotorEntity:
		""" Create Motor entity from Motor DTO """

		motor_entity = cls.map(
			from_obj=motor_dto,
			to_obj=MotorEntity,
			mapping={
				"v_nom": "voltage",
			},
			missing_values={
				"hp_nom": motor_dto.kw * 1.34,
				"eff_fl": 1,
				"pf_fl": 1
			}
		)

		return motor_entity

	@classmethod
	def create_dto(cls, motor_entity: MotorEntity):
		""" Create Motor DTO from Motor entity """

		motor_dto = cls.map(
			from_obj=motor_entity,
			to_obj=MotorDTO,
			mapping={
				"voltage": "v_nom",
			}
		)

		return motor_dto
