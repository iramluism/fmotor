""" Fmotor Infrastructure Repositories Module """

from typing import List
from dependency_injector.wiring import Provide

from src.seedwork.infrastructure.repositories import IRepository
from src.fmotor.domain.entities import VoltageRangeEntity

from .mappers import DBMotorMapper, DBVoltageRangeMapper, MotorAggregate
from .utils import get_voltage_ranges


class MotorRepository(IRepository):
	""" MotorRepository class """

	table_name = "nemamotors"

	_voltage_range_repository = Provide["voltage_range_repository"]

	def all(self):
		return self.filter()

	def filter(self, **filters) -> List[MotorAggregate]:

		_filters = DBMotorMapper.map_filters(filters)

		voltage_range = None
		if "v_nom" in filters:

			voltage_ranges_filter = \
				("in", get_voltage_ranges(filters.get("v_nom")))

			_filters["voltage_id"] = voltage_ranges_filter

			voltage_ranges = \
				self._voltage_range_repository.filter(id=voltage_ranges_filter)

			if voltage_ranges:
				voltage_range = voltage_ranges[0]

		motors = self.db.get_list(self.table_name, _filters, as_dict=True)
		return DBMotorMapper.create_aggregates(motors, voltage_range)

	def get(self, motor_id) -> MotorAggregate:
		motors = self.db.get_list(
			self.table_name, {"motor_id": motor_id}, as_dict=True, length=1)

		motor = None
		if motors:
			motor = DBMotorMapper.create_aggregate(motors[0])

		return motor


class VoltageRangeRepository(IRepository):
	""" VoltageRangeRepository class """

	voltage_table_name = "voltage_id"

	def get(self, voltage_id) -> VoltageRangeEntity:
		""" Get voltage Range entity by the voltage id """
		voltages = self.filter(voltage_id=voltage_id)
		if voltages:
			return voltages[0]

	def filter(self, **filters) -> List[VoltageRangeEntity]:
		""" Filter voltages ranges """
		filters = DBVoltageRangeMapper.map_filters(filters)
		voltages = self.db.get_list(self.voltage_table_name, filters, as_dict=True)
		return DBVoltageRangeMapper.create_entities(voltages)
