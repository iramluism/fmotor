""" Containers Interfaces Module """

from dependency_injector import containers, providers
from src.seedwork.ui.utils import get_running_app

from src.config import settings


class IContainer(containers.DeclarativeContainer):
	""" IContainer class """

	wiring_config = containers.WiringConfiguration(
		modules=[
			"src.seedwork.ui.app",
			"src.seedwork.ui.view_models",
			"src.seedwork.ui.builder",
			"src.seedwork.infrastructure.repositories"
		]
	)

	database_config = settings.DATABASE.get("default")

	db = providers.Singleton(database_config.get("engine"), database_config.get("path"))
	component_cache = providers.Singleton("src.seedwork.ui.cache.ComponentCache")
	builder = providers.Singleton("src.seedwork.ui.builder.IBuilder")
	ui_theme = providers.Singleton("src.seedwork.ui.themes.IDarkTheme")
	current_app = providers.Callable(get_running_app)

