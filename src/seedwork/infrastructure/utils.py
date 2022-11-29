""" Fmotor Infrastructure Utils Module """

from pypika import Table, Query, Field
from typing import Union, Iterable, Optional


def build_query(table_name: str, filters: Optional[dict] = None,
                fields: Optional[dict] = None):

	table = Table(table_name)

	if not fields:
		fields = "*"

	query = Query.from_(table).select(fields)

	if filters:
		conditions = build_conditions(filters)
		query = query.where(conditions)

	return str(query)


def build_conditions(filters: dict):

	operations_map = {
		"==": Field.eq,
		"!=": Field.ne,
		">=": Field.gte,
		">": Field.gt,
		"<=": Field.lte,
		"<": Field.lt,
		"in": Field.isin,
		"not in": Field.notin,
		"between": Field.between
	}

	conditions = None

	for fieldname, _filter in filters.items():
		field = Field(fieldname)
		op, value = parse_filter(_filter)

		operation = operations_map.get(op)
		if not operation:
			raise TypeError("Operator '%s' is not valid" % op)

		cond = operation(field, value)

		if not conditions:
			conditions = cond
		else:
			conditions &= cond

	return conditions


def parse_filter(_filter: Union[str, Iterable]):
	op = "=="
	value = _filter

	if isinstance(_filter, (tuple, list)):
		op = _filter[0]
		value = _filter[1]

	return op, value
