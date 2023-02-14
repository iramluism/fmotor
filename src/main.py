

from fmotor.ui.app import FMotorApp
from config import settings
import inject


def main():
	app = FMotorApp()
	app.build_config(settings)
	app.run()


if __name__ == "__main__":
	inject.configure_once()
	main()
