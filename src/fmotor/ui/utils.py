""" Fmotor UI Utils Module """


def convert(value, to, default=None):
	""" Convert string value to another type
	:param value: string
	:param to: class to convert
	:param default: default value if raise a value error on converting
	"""

	try:
		return to(value)
	except ValueError:
		return default or to()


def prepare_motor_values(motor: dict) -> dict:
	""" check all motors fields, and prepare all values """

	for field in ("eff_fl", "eff_75", "eff_50", "eff_25",
	              "pf_fl", "pf_75", "pf_50", "pf_25"):

		value = motor.get(field)
		if value:
			motor[field] = round(value, 2)
	return motor
