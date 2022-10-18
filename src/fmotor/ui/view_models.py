""" FMotor UI View Model Module """

from dependency_injector.wiring import Provide

from src.seedwork.ui.view_models import IViewModel
from src.fmotor.ui.dtos import (
	FilterMotorViewModelDTO,
	MotorDetailViewModelDTO,
	FilterMotorViewModelDTI,
	MotorDetailViewModelDTI,
	EstimateMotorPropertiesViewModelDTI,
	EstimateMotorPropertiesViewModelDTO,
	CalculateMotorPropertiesViewModelDTI,
	CalculateMotorPropertiesViewModelDTO
)


from src.fmotor.ui.components import (
	FilterMotorDialogComponent,
	MotorItemDialogComponent,
	MotorDetailDialogComponent
)


class EstimateMotorPropertiesViewModel(IViewModel):
	""" EstimateMotorPropertiesViewModel class """

	@classmethod
	def execute(cls, motor_properties: EstimateMotorPropertiesViewModelDTI
	            ) -> EstimateMotorPropertiesViewModelDTO:

		return EstimateMotorPropertiesViewModelDTO()


class CalculateMotorPropertiesViewModel(IViewModel):
	""" CalculateMotorPropertiesViewModel class """

	@classmethod
	def execute(cls, motor_properties: CalculateMotorPropertiesViewModelDTI
	            ) -> CalculateMotorPropertiesViewModelDTO:
		return CalculateMotorPropertiesViewModelDTO()


class GetMotorDetailViewModel(IViewModel):
	""" GetMotorDetailViewModel class """

	dialog_component = MotorDetailDialogComponent

	@classmethod
	def execute(cls, motor_detail: MotorDetailViewModelDTI
	            ) -> MotorDetailViewModelDTO:
		""" Get Motor Details """

		motor_detail_dto = MotorDetailViewModelDTO(
			motor_id=5, model="dsfss", catalog="sdfdsf")

		dialog = cls.dialog_component.build(
			motor_details=motor_detail_dto.as_dict())

		dialog.open()

		return motor_detail_dto


class FilterMotorViewModel(IViewModel):
	""" FilterMotorViewModel class """

	plot_motor_detail_view_model = Provide["plot_motor_detail_view_model"]

	filter_motor_dialog_component = FilterMotorDialogComponent
	filter_motor_item_dialog_component = MotorItemDialogComponent

	@classmethod
	def execute(cls, motor_filters: FilterMotorViewModelDTI
	            ) -> FilterMotorViewModelDTO:

		motors = [MotorDetailViewModelDTO(a,m,d) for a, m, d in [(1,"motor1", "description1"), (2, "motor2", "description2"), (3, "motor3", "description3"), (4, "motor1", "description1"), (5, "motor2", "description2"), (6, "motor3", "description3"), (7, "motor1", "description1"), (8, "motor2", "description2"), (9, "motor3", "description3")]]

		items = []

		for motor_dto in motors:
			item = cls.filter_motor_item_dialog_component.build(
				motor_id=motor_dto.motor_id,
				text=motor_dto.model,
				secondary_text=motor_dto.catalog
			)
			item.bind(on_press=cls.plot_motor_detail_view_model.execute)
			items.append(item)

		dialog = cls.filter_motor_dialog_component.build(items=items)
		dialog.open()

		return FilterMotorViewModelDTO(motors)
