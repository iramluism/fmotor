

from fmotor.ui.app import FMotorApp
from config.dependencies import Container
from config import settings


def main():
	app = FMotorApp()
	app.build_config(settings)
	app.run()


if __name__ == "__main__":
	container = Container()
	main()
