""" Fmotor UI DTOs Modules """

import dataclasses

from typing import List

from src.seedwork.infrastructure.dtos import IDTO


@dataclasses.dataclass
class MotorDetailViewModelDTO(IDTO):
	""" Motor Detail View Model Data Transfer Object """
	motor_id: int
	model: str
	catalog: str


@dataclasses.dataclass
class MotorDetailViewModelDTI(IDTO):
	"""Motor Detail View Model Data Transfer Input """
	motor_id: int


@dataclasses.dataclass
class FilterMotorViewModelDTO(IDTO):
	""" Filter Motor View Model Data Transfer Object """
	motors: List[MotorDetailViewModelDTO]


@dataclasses.dataclass
class FilterMotorViewModelDTI(IDTO):
	""" Filter Motor View Model Data Transfer Input """
	model: str
	catalog: str


@dataclasses.dataclass
class EstimateMotorPropertiesViewModelDTI(IDTO):
	""" Estimate Motor Properties Data Transfer Input """
	pass


@dataclasses.dataclass
class EstimateMotorPropertiesViewModelDTO(IDTO):
	""" Estimate Motor Properties Data Transfer Object """
	pass


@dataclasses.dataclass
class CalculateMotorPropertiesViewModelDTI(IDTO):
	""" Calculate Motor Properties Data Transfer Input """
	pass


@dataclasses.dataclass
class CalculateMotorPropertiesViewModelDTO(IDTO):
	""" Calculate Motor Properties Data Transfer Object """
	pass
