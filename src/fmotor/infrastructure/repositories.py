""" Fmotor Infrastructure Repositories Module """

from typing import List

from src.seedwork.infrastructure.repositories import IRepository
from src.fmotor.domain.entities import MotorEntity

from .mappers import DBMotorMapper


class MotorRepository(IRepository):
	""" MotorRepository class """

	table_name = "nemamotors"

	def save(self):
		pass

	def all(self):
		return self.filter()

	def filter(self, **filters) -> List[MotorEntity]:
		motors = self.db.get_list(self.table_name, filters, as_dict=True)
		return DBMotorMapper.create_entities(motors)

	def get(self, motor_id):
		motors = self.db.get_list(
			self.table_name, {"motor_id": motor_id}, as_dict=True, length=1)

		if motors:
			return motors[0]

	def create(self, *args, **kwargs):
		return MotorEntity(*args, **kwargs)

