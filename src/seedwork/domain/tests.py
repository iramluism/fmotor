import unittest

import dataclasses

from .mappers import IMapper


class MapperTestCase(unittest.TestCase):

	def setUp(self) -> None:

		self.class1 = type("class1", (object,), {
			"s_param1": 1, "s_param2": ("hola"), "s_param3": "hola",
			"s_param4": float(), "s_param5": object(), "s_param6": list(),
		})

		self.class2 = dataclasses.make_dataclass(
			"class2", [
				("param1", str),
				("param2", str),
				("param3", str),
				("param4", str),
				("param5", str),
				("param6", str),
			])

		return super().setUp()

	def test_get_fields_from_obj(self):

		obj1 = self.class1()

		fields = IMapper.get_fields(obj1)
		for f in ("s_param1", "s_param2", "s_param3",
		          "s_param4", "s_param5", "s_param6"):
			self.assertTrue(f in fields)

	def test_get_fields_classes(self):

		fields = IMapper.get_fields(self.class1)
		for f in ("s_param1", "s_param2", "s_param3",
		          "s_param4", "s_param5", "s_param6"):
			self.assertTrue(f in fields)

	def test_map_from_class(self):

		self.assertIsInstance(
			IMapper.map_objs(
				_from=self.class1, _to=self.class2,
				mapping={
					"param1": "s_param1",
					"param2": "s_param2",
					"param3": "s_param3",
					"param4": "s_param4",
					"param5": "s_param5",
					"param6": "s_param6",
				}
			),
			self.class2
		)

	def test_mutation_of_values_between_objects(self):

		obj1 = self.class1()

		mapping = {
			"param1": "s_param1",
			"param2": "s_param2",
			"param3": "s_param3",
			"param4": "s_param4",
			"param5": "s_param5",
			"param6": "s_param6"
		}

		obj2 = IMapper.map_objs(
			_from=obj1, _to=self.class2,
			mapping=mapping
		)

		self.assertIsInstance(obj2, self.class2)
		for _to, _from in mapping.items():

			value1 = getattr(obj1, _from)
			value2 = getattr(obj2, _to)

			if not isinstance(value1, (str, int, tuple, float)):
				self.assertNotEqual(id(value1), id(value2))

	def test_define_missing_values(self):

		obj2 = IMapper.map_objs(
			_from=self.class1(), _to=self.class2,
			mapping={
				"param1": "s_param1",
				"param2": "s_param2",
				"param3": "s_param3",
				"param4": "s_param4",
			},
			missing_values={
				"param5": 1,
				"param6": 2,
			}
		)

		self.assertEqual(obj2.param5, 1)
		self.assertEqual(obj2.param6, 2)

	def test_with_missing_values(self):
		with self.assertRaises(Exception):
			IMapper.map_objs(
				_from=self.class1(), _to=self.class2,
				mapping={
					"param1": "s_param1",
					"param2": "s_param2",
					"param3": "s_param3",
					"param4": "s_param4",
				},
				default_null=False,
				raise_if_missing=True
			)

	def test_fields_after_map_to_dict(self):

		obj = dataclasses.make_dataclass(
			"TestClass", [
				("param1", str, None),
				("param2", str, None),
				("param3", str, None),
				("param4", str, None),
				("param5", str, None),
				("param6", str, None),
			])()

		obj1_dict = IMapper.map_to_dict(obj)
		self.assertDictEqual(dataclasses.asdict(obj), obj1_dict)

	def test_excluded_field_after_map_to_dict(self):

		obj = dataclasses.make_dataclass(
			"TestClass", [
				("param1", str, None),
				("param5", str, None),
				("param6", str, None),
			])()

		obj_dict = IMapper.map_to_dict(obj, excluded_fields=["param6"])

		for field in obj_dict.keys():
			self.assertTrue(field in ("param1", "param5"))

	def test_map_to_dict_with_missing_values(self):

		obj = dataclasses.make_dataclass(
			"TestClass", [("param1", str, None)])()

		obj_dict = IMapper.map_to_dict(obj, missing_values={
			"param1": "random_value"
		})

		self.assertEqual(obj_dict.get("param1"), "random_value")

	def test_map_to_dict_with_default_values(self):

		obj = dataclasses.make_dataclass(
			"TestClass", [("param1", str, None)])()

		obj_dict = IMapper.map_to_dict(obj, default_values={
			"param1": "random_value"
		})

		self.assertEqual(obj_dict.get("param1"), "random_value")

	def test_priority_of_default_values_over_missing_values(self):

		obj = dataclasses.make_dataclass(
			"TestClass", [
				("param1", str, None),
				("param2", str, None),
				("param3", str, None),
			])()

		obj_dict = IMapper.map_to_dict(obj,
              default_values={
                  "param1": "value_1",
                  "param2": "value_2"
              },
              missing_values={
                  "param1": "value_1_on_missing",
                  "param3": "value_3"
              }
		)

		self.assertEqual(obj_dict.get("param1"), "value_1")
		self.assertNotEqual(obj_dict.get("param1"), "value_1_on_missing")
		self.assertEqual(obj_dict.get("param2"), "value_2")
		self.assertEqual(obj_dict.get("param3"), "value_3")

	def test_exchange_fields_on_mapping(self):

		test = {"a": 1, "b": 56, "c": 5}

		test_map = IMapper.map_to_dict(test, mapping={"d": "a"})

		self.assertNotIn("a", test_map)
		self.assertEqual(test_map.get("d"), 1)


if __name__ == '__main__':
	unittest.main()
