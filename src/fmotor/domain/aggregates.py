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
	eff_fl: float = None
	eff_75: float = None
	eff_50: float = None
	eff_25: float = None
	pf_fl: float = None
	pf_75: float = None
	pf_50: float = None
	pf_25: float = None
