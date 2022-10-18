
import abc


class IViewModel(metaclass=abc.ABCMeta):

	@classmethod
	@abc.abstractmethod
	def execute(cls, *args, **kwargs):
		pass
