""" Fmotor Domain Aggregates Module """

import dataclasses
from src.seedwork.domain.aggregates import IAggregate


@dataclasses.dataclass()
class MotorAggregate(IAggregate):
	""" Motor Aggregate """

	motor_id: int = None
	manufacturer_id: int = None
	voltage_id: int = None
	motor_type_id: int = None
	voltage: str = None
	v_nom: float = None
	rpm: float = None
	motor_type: str = None
	manufacturer: str = None
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
