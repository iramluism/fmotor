""" Fmotor Infrastructure Mappers Module """

from typing import List, Optional

from src.seedwork.domain.mappers import IMapper
from src.fmotor.domain.entities import VoltageRangeEntity, ManufacturerEntity
from src.fmotor.domain.aggregates import MotorAggregate
from .utils import get_voltage_from_id


class DBMotorMapper(IMapper):
	""" DBMotorMapper class """

	@classmethod
	def map_filters(cls, filters):
		""" map filters between motor aggregate fields
		and the fields on database """

		_filters = cls.map_to_dict(
			_from=filters,
			mapping={
				"motor_id": "id",
				"hp": "hp_nom",
				"nemadesign": "design"
			},
			missing_values={
				"hp": filters.get("kw", 0) * 1.341
			},
			excluded_fields=["v_nom"]
		)

		return _filters

	@classmethod
	def create_aggregate(cls, motor: Optional[dict] = None,
	                     voltage_range: Optional[dict] = None):
		""" Create aggregate from motor and voltage range saved on database """

		if not motor:
			motor = {}

		if not voltage_range:
			voltage_range = {}

		motor_aggregate = cls.map_objs(
			_from=motor, _to=MotorAggregate,
			mapping={
				"hp_nom": "hp",
				"i_idle": "amps_idle",
				"i_fl": "amps_fl",
				"design": "nemadesign"
			},
			default_values={
				"kw": float(motor.get("hp")) * 1.34,
				"v_nom": voltage_range.get("v_nom"),
				"voltage": voltage_range.get("description"),
			}
		)

		for field in MotorAggregate.field_details():
			value = motor_aggregate.get(field.name)
			if value:
				motor_aggregate.set(field.name, field.type(value))

		return motor_aggregate

	@classmethod
	def create_aggregates(cls, motors: Optional[List[dict]] = None,
	                      voltage_range: Optional[dict] = None):
		""" Create Aggregates from motor list saved on database """

		motor_entities = []
		for motor in motors:
			motor_entity = cls.create_aggregate(motor, voltage_range)
			motor_entities.append(motor_entity)

		return motor_entities


class DBVoltageRangeMapper(IMapper):
	""" DBVoltageRangeMapper class """

	@classmethod
	def map_filters(cls, filters):
		""" map filters between voltage range entity fields
		and the fields on database """
		return filters

	@classmethod
	def create_entity(cls, voltage: dict):
		""" Create entity form voltage saved on database """

		entity = cls.map_objs(
			_from=voltage, _to=VoltageRangeEntity,
			default_values={
				"v_nom": get_voltage_from_id(int(voltage.get("id", 0))),
			}
		)

		return entity


class DBManufacturerMapper(IMapper):
	""" DBManufacturerMapper class """

	@classmethod
	def map_filters(cls, filters):
		""" map filters between voltage range entity fields
		and the fields on database """

		_filters = cls.map_to_dict(
			_from=filters,
			mapping={
				"manufacturer_id": "id"
			}
		)

		return _filters

	@classmethod
	def create_entity(cls, manufacturer: dict):
		""" Create entity form voltage saved on database """

		entity = cls.map_objs(
			_from=manufacturer, _to=ManufacturerEntity,
			mapping={
				"id": "manufacturer_id",
			}
		)

		return entity
