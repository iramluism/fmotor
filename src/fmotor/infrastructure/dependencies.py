""" Fmotor Fmotor Dependencies Module """

from dependency_injector import containers, providers


class FMotorContainer(containers.DeclarativeContainer):
    """ FMotorContainer class """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "fmotor.ui.app",
            "fmotor.ui.view_models",
            "fmotor.ui.components",
            "fmotor.application.queries",
            "fmotor.application.commands",
            "fmotor.domain.services",
            "fmotor.infrastructure.repositories"
        ]
    )

    config = providers.Configuration()

    motor_cache = providers.Singleton("fmotor.ui.cache.MotorCache")

    estimate_motor_view_model = providers.Factory(
        "fmotor.ui.view_models.EstimateMotorViewModel"
    )

    calculate_motor_view_model = providers.Factory(
        "fmotor.ui.view_models.CalculateMotorViewModel"
    )

    filter_motor_view_model = providers.Factory(
        "fmotor.ui.view_models.FilterMotorViewModel")

    filter_motor_query = providers.Factory(
        "fmotor.application.queries.FilterMotorQuery",
    )

    motor_repository = providers.Factory(
        "fmotor.infrastructure.repositories.MotorRepository")

    manufacturer_repository = providers.Factory(
        "fmotor.infrastructure.repositories.ManufacturerRepository")

    voltage_range_repository = providers.Factory(
        "fmotor.infrastructure.repositories.VoltageRangeRepository")

    get_nearest_motor_service = providers.Factory(
        "fmotor.domain.services.GetNearestMotorService")

    motor_validator = providers.Factory(
        "fmotor.domain.validations.MotorValidator")

    get_motor_error_service = providers.Factory(
        "fmotor.domain.services.GetMotorErrorService")

    estimate_motor_command = providers.Factory(
        "fmotor.application.commands.EstimateMotorCommand")

    estimate_motor_service = providers.Factory(
        "fmotor.domain.services.EstimateMotorService")

    interpolate_motor_service = providers.Factory(
        "fmotor.domain.services.InterpolateMotorService")

    calculate_motor_command = providers.Factory(
        "fmotor.application.commands.CalculateMotorCommand")

    interpolate_motor_validator = providers.Factory(
        "fmotor.domain.validations.InterpolateMotorValidator")

