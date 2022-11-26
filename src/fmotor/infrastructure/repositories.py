""" Fmotor Infrastructure Repositories Module """

from typing import List

from src.seedwork.infrastructure.repositories import IRepository
from src.fmotor.domain.entities import MotorEntity

from .utils import parse_filter, eval_filter


class MotorRepository(IRepository):
	""" MotorRepository class """

	def save(self):
		pass

	def all(self):
		pass

	def filter(self, **filters) -> List[MotorEntity]:
		motors = []
		for motor in self.all():

			results = []
			for field, _filter in filters.items():
				op, value = parse_filter(_filter)
				result = eval_filter(motor.get(field), op, value, locals())
				results.append(result)

			if all(results):
				motors.append(motor)

		return motors

	def get(self, motor_id):
		motors = self.filter(id=motor_id)
		if motors:
			return motors[0]

	def create(self, *args, **kwargs):
		return MotorEntity(*args, **kwargs)

