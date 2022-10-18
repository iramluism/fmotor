""" FMotor UI App Module """

from dependency_injector.wiring import Provide

from src.seedwork.ui.app import IApp

from src.fmotor.ui.components import (
	FMotorAppComponent
)

from src.fmotor.ui.dtos import (
	MotorDetailViewModelDTI,
	FilterMotorViewModelDTI
)


from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp


class FMotorApp(IApp):
	""" FMotorApp class """

	_get_motor_detail_view_model = Provide["get_motor_detail_view_model"]
	_filter_motor_view_model = Provide["filter_motor_view_model"]

	def build(self):
		""" Build Fmotor Application """

# 		layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
# 		# Make sure the height is such that there is something to scroll.
# 		layout.bind(minimum_height=layout.setter('height'))
# 		for i in range(100):
# 			btn = Button(text=str(i), size_hint_y=None, height=40)
# 			layout.add_widget(btn)
# 		root = ScrollView(size_hint=(1, None),
# 		                  size=(Window.width, Window.height))
# 		root.add_widget(layout)
#
# 		from kivy.lang.builder import Builder
#
# 		Builder.load_string("""
# ScrollView:
#     do_scroll_x: False
#     do_scroll_y: True
#
#     Label:
#         size_hint_y: None
#         height: self.texture_size[1]
#         text_size: self.width, None
#         padding: 5, 5
#         text: 'sdfdsfsdf'
#
# 		""")
# 		return root

		return FMotorAppComponent.build()

	def open_motor_detail_dialog(self, motor):
		""" Show dialog details on Dialog
		:param motor: selected motor item component
		"""

		self._get_motor_detail_view_model.execute(
			MotorDetailViewModelDTI(motor.component.motor_id))

	def open_similar_motors_dialog(self):
		""" Show motors according to the filter """

		self._filter_motor_view_model.execute(
			FilterMotorViewModelDTI(catalog="sdfsdf", model="sdfsd")
		)

