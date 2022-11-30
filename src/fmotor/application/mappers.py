""" Fmotor Application Mappers Module """

from src.seedwork.domain.mappers import IMapper

from .dtos import MotorDTO, CalculateMotorDTO
from src.fmotor.domain.entities import MotorEntity, MotorMeasurement
from src.fmotor.domain.aggregates import MotorAggregate
from .utils import encrypt_motor_id, decrypt_motor_id


class MotorMapper(IMapper):
	""" MotorMapper class """

	@classmethod
	def create_aggregate(cls, motor_dto: MotorDTO) -> MotorAggregate:
		""" Create Motor entity from Motor DTO """

		default_values = {}
		if motor_dto.kw and not motor_dto.hp_nom:
			default_values["hp_nom"] = motor_dto.kw * 1.34
		elif motor_dto.hp_nom and not motor_dto.kw:
			default_values["kw"] = motor_dto.hp_nom / 1.34

		if motor_dto.id:
			default_values["motor_id"] = decrypt_motor_id(motor_dto.id)

		motor_entity = cls.map_objs(
			_from=motor_dto,
			_to=MotorAggregate,
			mapping={
				"motor_type": "type"
			},
			default_values=default_values
		)

		return motor_entity

	@classmethod
	def create_dto(cls, motor_aggr: MotorAggregate) -> MotorDTO:
		""" Create Motor DTO from Motor entity """

		motor_dto = cls.map_objs(
			_from=motor_aggr,
			_to=MotorDTO,
			mapping={
				"type": "motor_type",
			},
			default_values={
				"id": encrypt_motor_id(motor_aggr.motor_id)
			},
			excluded_fields=["manufacturer_id", "motor_type_id"]
		)

		return motor_dto


class MotorMeasurementMapper(IMapper):

	@classmethod
	def create_entity(cls, dto: CalculateMotorDTO):

		motor = MotorMapper.create_aggregate(dto.motor)

		entity = cls.map_objs(
			_from=dto, _to=MotorMeasurement,
			default_values={
				"motor": motor
			}
		)

		return entity

	@classmethod
	def create_dto(cls, entity):

		dto = cls.map_objs(_from=entity, _to=CalculateMotorDTO)
		return dto
