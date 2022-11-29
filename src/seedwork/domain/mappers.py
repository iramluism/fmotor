""" Maatai Core Mapper Module """

import copy
import dataclasses
import inspect
import re
from typing import Any, Optional


class IMapper:
	""" IMapper class """

	@classmethod
	def map_to_dict(cls, _from, mapping=None, excluded_fields=None, missing_values=None,
	                default_values=None):

		if not missing_values:
			missing_values = {}

		if not excluded_fields:
			excluded_fields = []

		if not default_values:
			default_values = {}

		to_fields = []

		from_fields = cls.get_fields(_from)
		for field in from_fields:
			if field in excluded_fields:
				continue

			to_fields.append((field, Any))

		to_obj_class = dataclasses.make_dataclass("to_obj_class", to_fields)

		to_obj = cls.map_objs(
			_from=_from, _to=to_obj_class,
			missing_values=missing_values,
			mapping=mapping,
			default_values=default_values,
		)

		return dataclasses.asdict(to_obj)

	@classmethod
	def map_objs(cls, _from: Any, _to: Any,
	             mapping: Optional[dict] = None,
	             missing_values: Optional[dict] = None,
	             default_values: Optional[dict] = None,
	             excluded_fields: Optional[list] = None,
	             raise_if_missing: bool = False
	             ):

		""" Map objects
		:param _from: source object to get values.
		:param _to: class or object to update values.
		:param mapping: fields to map between object, [to_obj, from_obj].
		:param missing_values: defined value is taken, if missing value.
		:param default_values: default values for new object
		:param excluded_fields: exclude fields on mapping process
		:param raise_if_missing: if not found at least one value, raise a error
		:return: new instance of _to class
        """

		properties = {}

		for field in cls.get_fields(_to):

			if excluded_fields and field in excluded_fields:
				continue

			if default_values and field in default_values:
				value = default_values[field]
			elif mapping and field in mapping:
				value = _from.get(mapping[field])
			else:
				value = _from.get(field)

			if not value and missing_values and field in missing_values:
				value = missing_values[field]

			if not value and raise_if_missing:
				raise Exception("missing %s field" % field)

			properties[field] = copy.deepcopy(value)

		if inspect.isclass(_to):
			to_obj = _to(**properties)
		else:
			to_obj = _to
			to_obj.__dict__.update(properties)

		return to_obj

	@staticmethod
	def get_fields(obj: Any) -> list:
		""" get all field of an object or a class"""

		if isinstance(obj, dict):
			return list(obj.keys())

		if dataclasses.is_dataclass(obj):
			return [field.name for field in dataclasses.fields(obj)]

		properties = []
		for field in dir(obj):
			value = getattr(obj, field)

			if not re.search(r"(^(\_)|\_$)", field) \
					and (not inspect.ismethod(value) or not inspect.isfunction(
				value)):
				properties.append(field)

		return properties
