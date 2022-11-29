""" Fmotor Domain Entities Module """

import dataclasses

from src.seedwork.domain.entities import IEntity


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
	eff_fl: float = 1
	eff_75: float = 1
	eff_50: float = 1
	eff_25: float = 1
	pf_fl: float = 1
	pf_75: float = 1
	pf_50: float = 1
	pf_25: float = 1
	id: int = None
