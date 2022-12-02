""" Fmotor Infrastructure Mappers Module """
import re
from typing import List, Optional

from seedwork.domain.mappers import IMapper
from fmotor.domain.entities import VoltageRangeEntity, ManufacturerEntity
from fmotor.domain.aggregates import MotorAggregate
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
				"hp": "p_nom",
				"nemadesign": "design",
				"rpm_fl": "rpm"
			},
			missing_values={
				"hp": filters.get("p_nom", 0) * 1341
			},
			excluded_fields=["v_nom"]
		)

		return _filters

	@classmethod
	def create_aggregate(cls, motor: Optional[dict] = None) -> MotorAggregate:
		""" Create aggregate from motor and voltage range saved on database """

		if not motor:
			motor = {}

		motor_aggregate = cls.map_objs(
			_from=motor, _to=MotorAggregate,
			mapping={
				"hp_nom": "hp",
				"i_idle": "amps_idle",
				"i_fl": "amps_fl",
				"design": "nemadesign",
				"rpm": "rpm_fl"
			},
			default_values={
				"p_nom": float(motor.get("hp", 0)) * 746.2686
			},
			missing_values={
				"eff_0": 0,
				"pf_0": 10,
			}
		)

		for field in MotorAggregate.field_details():
			value = motor_aggregate.get(field.name)

			if value:
				value = field.type(value)

				if re.search(r"(^eff\_)|(^pf\_)", field.name):
					value /= 100

				motor_aggregate.set(field.name, value)

		return motor_aggregate


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
