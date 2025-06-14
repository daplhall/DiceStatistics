from collections import defaultdict
from typing import Iterable

import dicechanics as ds
from dicechanics._math import unique


def sort_dict(faces: dict) -> dict:
	return dict(sorted(faces.items(), key=lambda pair: pair[0]))


def expand_dice(data: dict) -> dict:
	"""
	expands dice in a dictionary, to a dict of numbers
	"""
	dice = defaultdict(
		int, filter(lambda x: isinstance(x[0], ds.Die), data.items())
	)
	numbers = defaultdict(int, filter(lambda x: x[0] not in dice, data.items()))
	for i, die in enumerate(dice):
		for f in numbers.keys():
			numbers[f] *= die._units
		for d in dice:  # TODO THIS IS A PERFORMANCE HOG!!
			if d != die:
				dice[d] *= die._units
	for die, c in dice.items():
		for f, cd in die.items():
			numbers[f] += c * cd
	return numbers


def clean_faces(faces: dict) -> dict:
	faces = sort_dict(faces)
	return expand_dice(faces)


def collect_faces(faces: Iterable[float]) -> dict:
	out = dict(zip(*unique(faces)))
	return clean_faces(out)
