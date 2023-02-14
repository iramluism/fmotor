""" Fmotor UI Utils Module """


def convert(value, to, default=None):
	""" Convert string value to another type
	:param value: string
	:param to: class to convert
	:param default: default value if raise a value error on converting
	"""

	result = default or to()

	if value:
		try:
			result = to(value)
		except ValueError:
			pass

	return result


def prepare_motor_values(motor: dict) -> dict:
	""" check all motors fields, and prepare all values """

	for field, value in motor.items():
		if isinstance(value, (float, int)):
			motor[field] = round(value, 2)

	return motor


def parse_error_messages(e) -> list:
	""" Get error message from exception
	:param e: Exception instance
	"""

	messages = []
	errors = e.args[0]

	if isinstance(errors, str):
		errors = [errors]

	for error in errors:
		if isinstance(error, str):
			messages.append(error)

		elif "message" in error:
			messages.append(error.get("message"))

	return messages
