""" App UI SeedWork Module """

from kivymd.app import MDApp
from kivy.config import Config

from dependency_injector.wiring import Provide
from .components import IComponent


class IApp(MDApp):
	""" Interface UI App """

	builder = Provide["builder"]
	ui_theme = Provide["ui_theme"]
	root_component = None

	def build(self):
		""" build components on runtime """

		self.builder.build_component(IComponent)

		result_component = self.builder.get_result()
		return result_component.widget

	def on_start(self):
		""" Setup properties on app starting """

		self.theme_cls.theme_style = self.ui_theme.style
		# self.theme_cls.material_style = self.ui_theme.material_style
		self.theme_cls.primary_palette = self.ui_theme.primary_palette

	def load_settings(self, file):
		self.build_config(file)

	def on_stop(self): ...

	def on_pause(self): ...

	def on_resume(self): ...
