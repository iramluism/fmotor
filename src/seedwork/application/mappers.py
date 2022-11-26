""" Mapper Interfaces Module """

import abc


class IMapper(metaclass=abc.ABCMeta):

	@staticmethod
	def map(*, from_obj, to_obj, mapping=None, missing_values=None):

		missing_values = missing_values or {}
		mapping = mapping or {}

		to_obj_values = dict.fromkeys(to_obj.fields())

		for field in to_obj.fields():
			value = None

			from_obj_field = mapping.get(field) or field
			if from_obj_field in from_obj.fields():
				value = from_obj.get(from_obj_field)

			to_obj_values[field] = value or missing_values.get(field)

		entity = to_obj(**to_obj_values)

		return entity
