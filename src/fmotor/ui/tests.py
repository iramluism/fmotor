import unittest

from .utils import convert


class ConvertInputTestCase(unittest.TestCase):

	def test_convert_to_string(self):
		value = "Random value"
		self.assertEqual(convert(value, str), value)

	def test_convert_to_int(self):
		self.assertEqual(convert("12", int), 12)

	def test_convert_to_float(self):
		self.assertEqual(convert("12.3", float), 12.3)

	def test_convert_to_string_from_null_value(self):
		self.assertEqual(convert("", int), 0)

	def test_convert_to_int_from_null_value(self):
		self.assertEqual(convert("", float), 0.0)

	def test_not_convert_and_get_default_value(self):
		self.assertEqual(convert("random", int, "default value"), "default value")


if __name__ == '__main__':
	unittest.main()
