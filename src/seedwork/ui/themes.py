
import abc


class ITheme(metaclass=abc.ABCMeta):
	style: str
	material_style: str
	primary_palette: str


class IDarkTheme(ITheme):
	style = "Light"
	material_style = "M3"
	primary_palette = "LightBlue"
