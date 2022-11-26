""" App UI Interface Module """

from kivymd.app import MDApp

from dependency_injector.wiring import Provide


class IApp(MDApp):
	""" Interface UI App """

	builder = Provide["builder"]
	ui_theme = Provide["ui_theme"]

	def build(self):
		pass

	def on_start(self):
		""" Setup properties on app starting """
		self.theme_cls.theme_style = self.ui_theme.style
		self.theme_cls.material_style = self.ui_theme.material_style
		self.theme_cls.primary_palette = self.ui_theme.primary_palette

	def on_stop(self): ...

	def on_pause(self): ...

	def on_resume(self): ...
