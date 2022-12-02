""" Infrastructure Databases Module """

import sqlite3
import abc

from typing import Optional
from config import settings

from .utils import build_query


class DatabaseManager(metaclass=abc.ABCMeta):
	""" DatabaseManager class """

	db_config = settings.DATABASE or {}

	def __init__(self, db_path=None):
		config = self.get_config()

		if not db_path:
			db_path = config.get("path")

		self.db_path = db_path

	def get_config(self):
		return self.db_config.get("default")


class SQLiteManager(DatabaseManager):
	""" SQLiteManager class """

	_conn = None
	_cur = None

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

		return result

	def close(self):
		""" close cursor connection """
		if self._cur:
			self._cur.close()

	def connect(self):
		self._conn = sqlite3.connect(self.db_path)

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

