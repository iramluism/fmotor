""" Fmotor Domain Utils Module """

import math

from typing import Iterable, Optional


def linear_interpolation(
		p1: Iterable[float], p2: Iterable[float], x: float) -> float:
	"""
	Calculate Linear interpolation between two points
	:param p1: first point (x1, y1)
	:param p2: second point (x2, y2)
	:param x: value to interpolate
	"""

	x1, y1 = p1
	x2, y2 = p2

	y = (y2 - y1) / (x2 - x1) * (x - x1) + y1

	return y
