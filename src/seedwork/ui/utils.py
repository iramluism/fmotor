
from .events import State, StateObserver


def get_state(initial_state):

	event = StateObserver()
	event.state = State(initial_state)
	return event.state, event


def get_running_app():
	from .app import IApp
	return IApp.get_running_app()


def get_component(_id):
	app = get_running_app()
	return app.root.ids.get(_id)
