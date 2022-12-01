""" Fmotor Domain Entities Module """

import dataclasses

from seedwork.domain.entities import IEntity


@dataclasses.dataclass()
class MotorEntity(IEntity):
	""" Motor Entity """

	rpm: float = None
	motor_type: str = None
	manufacturer_id: str = None
	model: str = None
	catalog: str = None
	frame: str = None
	design: str = None
	hp_nom: float = None
	kw: float = None
	i_idle: float = None
	i_fl: float = None
	i_75: float = None
	i_50: float = None
	i_25: float = None
	eff_fl: float = 1
	eff_75: float = 1
	eff_50: float = 1
	eff_25: float = 1
	pf_fl: float = 1
	pf_75: float = 1
	pf_50: float = 1
	pf_25: float = 1
	id: int = None


@dataclasses.dataclass()
class VoltageRangeEntity(IEntity):
	description: str
	match_list: str
	v_nom: float = None
	id: int = None


@dataclasses.dataclass()
class ManufacturerEntity(IEntity):
	name: str
	id: int = None


@dataclasses.dataclass()
class MotorMeasurement(IEntity):
	motor: MotorEntity
	current: float
	v: float = None
	kc: float = None
	pf: float = None
	eff: float = None
	p_out: float = None
	p_in: float = None
	losses: float = None
