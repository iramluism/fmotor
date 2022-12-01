
from dependency_injector import containers, providers

from fmotor.infrastructure.dependencies import FMotorContainer
from seedwork.infrastructure.dependencies import IContainer


class Container(containers.DeclarativeContainer):

	seedwork = providers.Container(IContainer)
	f_motor = providers.Container(FMotorContainer)

