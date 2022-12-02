""" FMotor UI App Module """

from seedwork.ui.app import IApp

from .components import FMotorAppComponent


class FMotorApp(IApp):
	""" FMotorApp class """

	def build(self):
		""" Build Fmotor Application """
		return FMotorAppComponent.build()

	def on_pause(self):
		return True
