""" Theme Interfaces Module """

import abc
from kivy.utils import get_color_from_hex


class ITheme(metaclass=abc.ABCMeta):
	style: str
	material_style: str
	primary_palette: str


class IDarkTheme(ITheme):
	style = "Light"
	material_style = "M3"
	primary_palette = "LightBlue"
	overlay_color = get_color_from_hex("#6042e4")
