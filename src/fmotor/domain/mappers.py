""" Fmotor Domain Mappers Module """

from src.seedwork.domain.mappers import IMapper
from .entities import MotorEntity


class EstimateMotorMapper(IMapper):
	""" EstimateMotorMapper class """

	@classmethod
	def create_motor(cls, motor_eval: MotorEntity, motor_ref: MotorEntity
	                 ) -> MotorEntity:
		""" Create motor from two motors """

		motor = cls.map_objs(
			_from=motor_eval, _to=MotorEntity,
			missing_values={
				"v_nom": motor_ref.v_nom,
				"rpm": motor_ref.rpm,
				"hp_nom": motor_ref.hp_nom,
				"kw": motor_ref.kw,
				"eff_fl": motor_ref.eff_fl,
				"eff_75": motor_ref.eff_75,
				"eff_50": motor_ref.eff_50,
				"eff_25": motor_ref.eff_25,
				"pf_fl": motor_ref.pf_fl,
				"pf_75": motor_ref.pf_75,
				"pf_50": motor_ref.pf_50,
				"pf_25": motor_ref.pf_25
			},
			excluded_fields=["model", "manufacturer", "design",
			                 "frame", "motor_type"]
		)

		return motor
