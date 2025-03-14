import unittest
import numpy as np

import DiceStatistics as tts
import dice_unittest

class TestDiceConstructor(dice_unittest.TestCase):
	def test_construct_number(self):
		d = tts.d(5)
		self.assertSequenceEqual(d.f, [1,2,3,4,5])

	def test_construct_Znumber(self):
		d = tts.z(5)
		self.assertSequenceEqual(d.f, [0,1,2,3,4,5])

	def test_construct_text1(self):
		d = tts.d("1,2,3,4,5,6")
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])

	def test_construct_text2(self):
		d = tts.d("1,2,3..6,9")
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6,9])

	def test_construct_text_count(self):
		d = tts.d("1,2,3,3,4")
		self.assertSequenceEqual(d.f, [1,2,3,4])
		self.assertSequenceAlmostEqual(d.p, [0.2,0.2,0.4,0.2], 2)

	def test_construct_iterable(self):
		d = tts.d(i for i in range(1, 7))
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(d.p, [0.1667]*6, 4)
	
	def test_copy(self):
		d = tts.d("1..5:4,20,20,31")
		g = d.copy()
		self.assertSequenceEqual(d.f, g.f)
		self.assertSequenceEqual(d.c, g.c)
		self.assertSequenceAlmostEqual(d.p, g.p, 10)
		
	def test_decorator(self):
		@tts.d('5..6:3,6,6')
		def funky_dice(faces):
			if faces == 1:
				return 32
			elif faces == 6:
				return 42
			else:
				return -1
		
		d = funky_dice()
		self.assertSequenceEqual(d.f, [-1,42])
		self.assertSequenceAlmostEqual(d.p, [0.3750, 0.6250], 4)

	def test_decorator_d6(self):
		@tts.d('1..6')
		def funky_dice(faces):
			if faces == 6:
				return tts.d6
			else:
				return faces
		
		d = funky_dice()
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			d.p, 
			[0.1944]*5 + [0.0278], 
			4
		)

	def test_decorator_d6_to_d4(self):
		@tts.d('1..6')
		def funky_dice(faces):
			if faces == 6:
				return tts.d4
			else:
				return faces
		
		d = funky_dice()
		self.assertSequenceEqual(d.f, [1,2,3,4,5])
		self.assertSequenceAlmostEqual(
			d.p, 
			[0.2083]*4 + [0.1667], 
			4
		)

class TestPool(dice_unittest.TestCase):
	def test_constructor(self):
		d6 = tts.d6
		pool = tts.Pool([d6,d6])
		self.assertSequenceEqual(pool.f, [2,3,4,5,6,7,8,9,10,11,12])
		self.assertSequenceAlmostEqual(pool.f, 
			[0.0278,0.0556,0.0833,0.1111,0.1389,
				0.1667,0.1389,0.1111,0.0833,0.0556,0.0278],
			4
		)

	def test_constructor_3dice(self):
		d6 = tts.d6
		d8 = tts.d8
		pool = tts.Pool([d6, d8, d6])
		self.assertEqual(1,0)

	

if __name__ == '__main__':
	unittest.main()