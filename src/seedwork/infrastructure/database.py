""" Infrastructure Databases Module """

import sqlite3
import abc

from typing import Optional

from .utils import build_query


class DatabaseManager(metaclass=abc.ABCMeta):
	""" DatabaseManager class """

	@abc.abstractmethod
	def execute(self, *args, **kwargs):
		pass


class SQLiteManager(DatabaseManager):
	""" SQLiteManager class """

	def __init__(self, db_path):
		self.db_path = db_path
		self._conn = None
		self._cur = None

	def close(self):
		""" close cursor connection """
		if self._cur:
			self._cur.close()

	def connect(self):
		self._conn = sqlite3.connect(self.db_path)

	def get_list(self, table, filters: Optional[dict] = None,
	             fields: Optional[dict] = None, as_dict: bool = False,
	             length: Optional[int] = None) -> list:
		""" Get report list
		:param table: Table name
		:param filters: conditions
		:param fields: fields to select
		:param as_dict: return each report in dict format
		:param length: maximum reports number
		"""
		query = build_query(table, filters, fields)
		response = self.execute(query)

		if as_dict:
			result = self._convert_response_to_dict(response)
		else:
			result = response.fetchall()

		result = result[:length]

		self.close()
		return result

	@staticmethod
	def _convert_response_to_dict(response):
		""" Convert response to dict """
		results = []
		fields_props = response.description

		for row in response.fetchall():
			dict_result = {}
			for idx, value in enumerate(row):
				fieldname = fields_props[idx][0]
				dict_result[fieldname] = value
			results.append(dict_result)
		return results

	def execute(self, query: str):
		""" Execute sql query """

		self.connect()
		cur = self._conn.cursor()
		response = cur.execute(query)
		self._cur = cur
		return response

