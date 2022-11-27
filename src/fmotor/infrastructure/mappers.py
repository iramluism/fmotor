
from src.seedwork.domain.mappers import IMapper
from src.fmotor.domain.entities import MotorEntity


class DBMotorMapper(IMapper):

	@classmethod
	def create_entity(cls, motor: dict):

		motor_entity = cls.map_objs(
			_from=motor, _to=MotorEntity,
			mapping={
				"id": "motor_id",
				"manufacturer": "manufacturer_id"
			}
		)

		for field in MotorEntity.field_details():
			value = motor_entity.get(field.name)
			if value:
				motor_entity.set(field.name, field.type(value))

		return motor_entity

	@classmethod
	def create_entities(cls, motors):

		motor_entities = []
		for motor in motors:
			motor_entity = cls.create_entity(motor)
			motor_entities.append(motor_entity)

		return motor_entities
