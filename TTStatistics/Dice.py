from typing import Generator
from itertools import product
import operator as op
from TTStatistics._parser import faces_to_prop
from TTStatistics.types import primitives
from TTStatistics._math import ceildiv
import TTStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool


class Dice(object):
	def __init__(self, faces, /, mask = None, rounding = 'regular'):
		self._f, self._p, self._c = faces_to_prop(faces)		
		self._derived_attr()
		self._mask = mask if mask else None
		self._rounding = rounding

	def _derived_attr(self):
		self._mean = sum([p*f for p, f in zip(self.c, self.p)])
		self._cdf = self._cumulative()

	@property
	def f(self) -> list:
		return self._f
	@property
	def p(self) -> list:
		return self._p

	@property
	def c(self) -> list:
		return self._c
	
	@property
	def mean(self) -> float:
		return self._mean

	@property
	def cdf(self) -> list:
		return self._cdf

	def copy(self) -> Dice:
		copy = Dice(i for i in self)
		return copy
	
	def _number_binary(self, rhs: int | float, operations:callable):
		return Dice(operations(i, rhs) for i in self)
	
	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f
	# TODO i can do a rounding function that depeneds on the _rounding	
	def _binary_level0(self, rhs: int | float, ops: callable ) -> Dice | Pool:
		if isinstance(rhs, primitives):
			return Dice(ops(f, rhs) for f in self)
		elif isinstance(rhs, Dice):
			raise NotImplemented
		else: # This here should test the other way around.
			raise Exception("Unexpected type in dice level 0")

	def __add__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		"""
		only does level 0, if higher up we reverse the call.
		TODO rounding reaction
		"""
		return self._binary_level0(rhs, op.add)
	
	def __sub__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		# needs to reach to rounding
		return self._binary_level0(rhs, op.sub)

	def __mul__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		## Needs to react to rounding
		return self._binary_level0(rhs, op.mul)

	def __truediv__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		if self._rounding == 'regular':
			return self._binary_level0(rhs, op.truediv)
		elif self._rounding == 'down':
			return self._binary_level0(rhs, op.floordiv)
		elif self._rounding == 'up':
			return self._binary_level0(rhs, ceildiv)
		else:
			raise Exception("Rounding is defined as unsupporeted value::%s", self._rounding)


	def _cumulative(self) -> list:
		res = []
		for p in self.p: ## can fold this out an call with iter to clean up the if statement
			if res:
				res.append(p + res[-1])
			else:
				res.append(p)
		return res