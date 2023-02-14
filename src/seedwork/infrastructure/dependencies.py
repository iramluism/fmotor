""" Containers Interfaces Module """

from dependency_injector import containers, providers
from seedwork.ui.utils import get_running_app

from config import settings


class IContainer(containers.DeclarativeContainer):
	""" IContainer class """

	wiring_config = containers.WiringConfiguration(
		modules=[
			"seedwork.ui.app",
			"seedwork.ui.events",
			"seedwork.ui.view_models",
			"seedwork.ui.builder",
			"seedwork.infrastructure.repositories"
		]
	)

	database_config = settings.DATABASE.get("default")

	db = providers.Singleton(database_config.get("engine"), database_config.get("path"))
	component_cache = providers.Singleton("seedwork.ui.cache.ComponentCache")
	event_cache = providers.Singleton(
		"seedwork.ui.cache.EventCache")
	builder = providers.Singleton("seedwork.ui.builder.IBuilder")
	ui_theme = providers.Singleton("seedwork.ui.themes.IDarkTheme")
	current_app = providers.Callable(get_running_app)

