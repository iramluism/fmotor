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


def calculate_three_phase_current(p: float, v: float,
                                  eff: Optional[float] = None,
                                  pf: Optional[float] = None):
	""" Calculate Three Phase current
	:param p: power (watts)
	:param v: voltage (V)
	:param eff: efficiency, by default 1
	:param pf: power factor, by default 1
	"""

	eff = eff or 1
	pf = pf or 1
	current = p / (math.sqrt(3) * v * eff * pf)

	return current
