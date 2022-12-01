""" Translations Module """

import enum
from src.config import settings
from typing import Optional


class Language(enum.Enum):
	""" Languages Enum """
	ES = "es"
	EN = "en"


class Translator:
	""" Translator class """

	def __init__(self, lang: Optional[Language] = None):
		""" Setup Translator instance """

		self.config = settings.TRANSLATIONS
		self.sys_lang = settings.LANGUAGE

		if not lang:
			lang = self.sys_lang

		self.lang = lang.value

	def translate(self, text: str, lang: Optional[str] = None,
	              context: Optional[str] = None) -> str:
		""" translate text, otherwise return the same text.
		:param text: text to translate
		:param lang: language to translate, by default take the system language
		:param context: translate text according to context
		"""
		if not lang:
			lang = self.get_sys_lang()

		if self.sys_lang == self.lang:
			return text

		translations = self.get_translations(lang)

		text_key = self.get_text_key(text, context)
		translated_text = translations.get(text_key)

		return translated_text or text

	def get_translations(self, lang: str) -> dict:
		""" open translation file path and create a dict with
		all translations to lang
		"""
		lang_config = self.config.get(lang)
		path = lang_config.get("path")

		translations = {}
		with open(path, "r") as content:

			while content:
				line = content.readline()

				if not line:
					break

				line = line.replace("\n", "")
				translation = line.split(",")

				context = None

				from_text, to_text, *args = translation
				if args:
					context = args[0]

				text_key = self.get_text_key(from_text, context)

				translations[text_key] = to_text

		return translations

	@staticmethod
	def get_text_key(text, context=None):
		""" Create text key based on text and context """
		key_text = text
		if context:
			key_text += ":%s" % context

		return key_text

	def get_sys_lang(self):
		""" Get system language """
		return self.sys_lang or "en"
