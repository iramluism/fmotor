
from dependency_injector import containers, providers
from src.seedwork.ui.utils import get_running_app

class IContainer(containers.DeclarativeContainer):

	wiring_config = containers.WiringConfiguration(
		modules=[
			"src.seedwork.ui.app"
		]
	)

	builder = providers.Singleton("src.seedwork.ui.builder.IBuilder")
	root_component = providers.Factory("kivymd.uix.widget.MDWidget")
	ui_theme = providers.Singleton("src.seedwork.ui.themes.IDarkTheme")
	current_app = providers.Callable(get_running_app)

