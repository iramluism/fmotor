""" Fmotor Infrastructure Repositories Module """

import inject

from typing import List

from seedwork.infrastructure.repositories import IRepository
from fmotor.domain.entities import VoltageRangeEntity, ManufacturerEntity
from fmotor.domain.aggregates import MotorAggregate

from .mappers import DBMotorMapper, DBVoltageRangeMapper, DBManufacturerMapper
from .utils import get_voltage_ranges


class ManufacturerRepository(IRepository):
	""" ManufacturerRepository class """

	_table_name = "manufacturer"

	def get(self, _id) -> ManufacturerEntity:
		""" Get manufacturer entity """
		manufactures = self.db.get_list(
			self._table_name, {"manufacturer_id": _id}, as_dict=True, length=1)

		manufacturer = None
		if manufactures:
			manufacturer = DBManufacturerMapper.create_entity(manufactures[0])

		return manufacturer


class VoltageRangeRepository(IRepository):
	""" VoltageRangeRepository class """

	voltage_table_name = "voltage_id"

	def get(self, voltage_id) -> VoltageRangeEntity:
		""" Get voltage Range entity by the voltage id """

		voltages = self.db.get_list(
			self.voltage_table_name, {"id": voltage_id}, as_dict=True,
			length=1)

		voltage = None
		if voltages:
			voltage = DBVoltageRangeMapper.create_entity(voltages[0])

		return voltage


class MotorRepository(IRepository):
	""" MotorRepository class """

	table_name = "nemamotors"

	_voltage_range_repository = inject.attr(VoltageRangeRepository)
	_manufacturer_repository = inject.attr(ManufacturerRepository)

	def all(self):
		return self.filter()

	def filter(self, **filters) -> List[MotorAggregate]:

		_filters = DBMotorMapper.map_filters(filters)

		if "v_nom" in filters:

			voltage_ranges_filter = \
				("in", get_voltage_ranges(filters.get("v_nom")))

			_filters["voltage_id"] = voltage_ranges_filter

		db_motors = self.db.get_list(self.table_name, _filters, as_dict=True)

		motors = []
		for db_motor in db_motors:

			motor = DBMotorMapper.create_aggregate(db_motor)

			if motor.manufacturer_id:
				manufacturer = self._manufacturer_repository.get(
					motor.manufacturer_id)
				motor.manufacturer = manufacturer.name

			if motor.voltage_id:
				voltage = self._voltage_range_repository.get(motor.voltage_id)
				motor.voltage = voltage.description

			motors.append(motor)

		return motors

	def get(self, motor_id) -> MotorAggregate:
		motors = self.db.get_list(
			self.table_name, {"motor_id": motor_id}, as_dict=True, length=1)

		motor = None
		if motors:
			motor = DBMotorMapper.create_aggregate(motors[0])

		return motor