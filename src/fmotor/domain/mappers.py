""" Fmotor Domain Mappers Module """

from seedwork.domain.mappers import IMapper
from .aggregates import MotorAggregate


class EstimateMotorMapper(IMapper):
	""" EstimateMotorMapper class """

	@classmethod
	def create_motor(cls, motor_eval: MotorAggregate, motor_ref: MotorAggregate
	                 ) -> MotorAggregate:
		""" Create motor from two motors """

		motor = cls.map_objs(
			_from=motor_eval, _to=MotorAggregate,
			missing_values={
				"voltage": motor_ref.voltage,
				"i_idle": motor_ref.i_idle,
				"i_fl": motor_ref.i_fl,
				"eff_fl": motor_ref.eff_fl,
				"eff_75": motor_ref.eff_75,
				"eff_50": motor_ref.eff_50,
				"eff_25": motor_ref.eff_25,
				"pf_fl": motor_ref.pf_fl,
				"pf_75": motor_ref.pf_75,
				"pf_50": motor_ref.pf_50,
				"pf_25": motor_ref.pf_25
			},
		)

		return motor
