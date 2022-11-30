""" Fmotor Fmotor Dependencies Module """

from dependency_injector import containers, providers


class FMotorContainer(containers.DeclarativeContainer):
    """ FMotorContainer class """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.fmotor.ui.app",
            "src.fmotor.ui.view_models",
            "src.fmotor.ui.components",
            "src.fmotor.application.queries",
            "src.fmotor.application.commands",
            "src.fmotor.domain.services",
            "src.fmotor.infrastructure.repositories"
        ]
    )

    config = providers.Configuration()

    motor_cache = providers.Singleton("src.fmotor.ui.cache.MotorCache")

    estimate_motor_view_model = providers.Factory(
        "src.fmotor.ui.view_models.EstimateMotorViewModel"
    )

    calculate_motor_view_model = providers.Factory(
        "src.fmotor.ui.view_models.CalculateMotorViewModel"
    )

    filter_motor_view_model = providers.Factory(
        "src.fmotor.ui.view_models.FilterMotorViewModel")

    filter_motor_query = providers.Factory(
        "src.fmotor.application.queries.FilterMotorQuery",
    )

    motor_repository = providers.Factory(
        "src.fmotor.infrastructure.repositories.MotorRepository")

    voltage_range_repository = providers.Factory(
        "src.fmotor.infrastructure.repositories.VoltageRangeRepository")

    get_nearest_motor_service = providers.Factory(
        "src.fmotor.domain.services.GetNearestMotorService")

    motor_validator = providers.Factory(
        "src.fmotor.domain.validations.MotorValidator")

    get_motor_error_service = providers.Factory(
        "src.fmotor.domain.services.GetMotorErrorService")

    estimate_motor_command = providers.Factory(
        "src.fmotor.application.commands.EstimateMotorCommand")

    estimate_motor_service = providers.Factory(
        "src.fmotor.domain.services.EstimateMotorService")

    interpolate_motor_service = providers.Factory(
        "src.fmotor.domain.services.InterpolateMotorService")

    calculate_motor_command = providers.Factory(
        "src.fmotor.application.commands.CalculateMotorCommand")

    interpolate_motor_validator = providers.Factory(
        "src.fmotor.domain.validations.InterpolateMotorValidator")

