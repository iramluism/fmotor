""" Fmotor Infrastructure Utils Module """


def parse_filter(_filter):
	""" Parse filter value """

	op = "=="
	value = None

	if isinstance(_filter, (tuple, list)):
		op = _filter[0]
		value = _filter[1]

	return op, value


def eval_filter(ref, op, value, context=None):
	""" eval conditions """
	return eval("%s %s %s" % (ref, op, value), context)
