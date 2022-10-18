

from src.fmotor.ui.app import FMotorApp
from src.config.dependencies import Container
from src.config import settings


def main():
	app = FMotorApp()
	app.build_config(settings)
	app.run()


if __name__ == "__main__":
	container = Container()
	main()
