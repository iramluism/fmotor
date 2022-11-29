""" Fmotor Infrastructure Utils Module """


VOLTAGE_RANGES = {
	200: [2],
	208: [4, 5],
	220: [11],
	230: [4, 5, 12],
	440: [11],
	460: [6, 7, 12, 13],
	575: [8],
	796: [12, 13],
	2300: [9, 14],
	4000: [10, 14, 15],
	6600: [15]
}


def get_voltage_ranges(voltage):
	""" Return the max voltage range for a given voltage """

	max_v = get_max_voltage_range(voltage)
	voltage_range = VOLTAGE_RANGES.get(max_v)
	return voltage_range


def get_max_voltage_range(voltage):
	""" Find the max voltage that belong to a given voltage """

	for top_v_range in VOLTAGE_RANGES.keys():
		if voltage <= top_v_range:
			return top_v_range


def get_voltage_from_id(voltage_id):
	""" Find max voltage according to voltage id """

	max_v = None
	for voltage, voltage_range in VOLTAGE_RANGES.items():
		if voltage_id in voltage_range:
			max_v = voltage

	return max_v
