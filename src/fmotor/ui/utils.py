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
