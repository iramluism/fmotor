""" Fmotor Application DTOs Module """

import dataclasses

from seedwork.infrastructure.dtos import IDTO


@dataclasses.dataclass()
class MotorDTO(IDTO):
	""" Motor Data Transfer Object """

	rpm: float
	kw: float = None
	v_nom: str = None
	voltage: str = None
	hp_nom: float = None
	manufacturer: str = None
	model: str = None
	catalog: str = None
	frame: str = None
	design: str = None
	type: str = None
	p_nom: str = None
	i_idle: float = None
	i_fl: float = None
	i_75: float = None
	i_50: float = None
	i_25: float = None
	i_0: float = None
	eff_fl: int = None
	eff_75: int = None
	eff_50: int = None
	eff_25: int = None
	eff_0: int = None
	pf_fl: int = None
	pf_75: int = None
	pf_50: int = None
	pf_25: int = None
	pf_0: int = None
	id: str = None


@dataclasses.dataclass()
class FilterMotorQueryDTO(IDTO):
	""" Filter Motor Query Data Transfer Output """
	motors: list[MotorDTO] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class EstimateMotorDTI(IDTO):
	""" Estimate Motor Data Transfer Input """
	motor_eval: MotorDTO
	motor_ref: MotorDTO


@dataclasses.dataclass()
class CalculateMotorDTO(IDTO):

	motor: MotorDTO
	current: float
	kc: float = None
	pf: float = None
	eff: float = None
	p_out: float = None
	p_in: float = None
	losses: float = None

