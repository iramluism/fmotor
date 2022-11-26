""" Utils Module """

from .cache import ComponentCache
from .app import IApp


def get_running_app():
	""" Get the app that is running currently """
	return IApp.get_running_app()


def get_component(_id):
	""" Get Component from cache """
	cache = ComponentCache()
	component = cache.get(_id)
	return component
