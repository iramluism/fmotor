""" Fmotor Application DTOs Module """

import dataclasses

from src.seedwork.infrastructure.dtos import IDTO


@dataclasses.dataclass()
class MotorDTO(IDTO):
	""" Motor Data Transfer Object """

	voltage: float
	kw: float
	rpm: float
	motor_type: str = None
	manufacturer: str = None
	model: str = None
	catalog: str = None
	frame: str = None
	design: str = None
	type: str = None
	eff_fl: int = 1
	eff_75: int = None
	eff_50: int = None
	eff_25: int = None
	pf_fl: int = 1
	pf_75: int = None
	pf_50: int = None
	pf_25: int = None
	id: int = None


@dataclasses.dataclass()
class FilterMotorQueryDTO(IDTO):
	""" Filter Motor Query Data Transfer Output """
	motors: list[MotorDTO] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class EstimateMotorDTI(IDTO):
	""" Estimate Motor Data Transfer Input """
	motor_eval: MotorDTO
	motor_ref: MotorDTO


