from dependency_injector import containers, providers


class FMotorContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.fmotor.ui.app",
            "src.fmotor.ui.view_models",
        ]
    )

    config = providers.Configuration()

    filter_motor_view_model = providers.Factory(
        "src.fmotor.ui.view_models.FilterMotorViewModel")

    plot_motor_detail_view_model = providers.Factory(
        "src.fmotor.ui.view_models.GetMotorDetailViewModel")

    calculate_motor_properties_view_model = providers.Factory(
        "src.fmotor.ui.view_models.CalculateMotorPropertiesViewModel")

    estimate_motor_properties_view_model = providers.Factory(
        "src.fmotor.ui.view_models.EstimateMotorPropertiesViewModel")



