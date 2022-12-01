""" Utils Module """

from .cache import ComponentCache
from .app import IApp
from .translations import Translator, Language


def get_running_app():
	""" Get the app that is running currently """
	return IApp.get_running_app()


def get_component(_id):
	""" Get Component from cache """
	cache = ComponentCache()
	component = cache.get(_id)
	return component


def _(text, lang=None, *, context=None):
	""" Translate text to lang, otherwise return the same text
	:param text: text to translate
	:param lang: (es, en, etc ..), by default take the system language
	:param context: translate text according to context
	"""

	translator = Translator(Language.EN)
	translated_text = translator.translate(text, lang, context)

	return translated_text
