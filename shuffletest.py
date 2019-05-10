import unittest
from shuffle import DivideAndOverShuffle, CutAndMergeShuffle, RandomShuffle

def _repeated_twice(self, originalCards, shuffling_algorithm):
		shuffledCards = shuffling_algorithm.shuffle(originalCards)
		shuffledCards = shuffling_algorithm.shuffle(shuffledCards)
		
		shuffledCardsTwice = shuffling_algorithm.shuffle(originalCards, 2)
		self.assertSequenceEqual(shuffledCards, shuffledCardsTwice)

class DivideAndOverShuffleTest(unittest.TestCase):
	def test_3_part_shuffle_divisible_by_3(self):
		originalCards = [1,2,3];

		shuffling_algorithm = DivideAndOverShuffle()
		shuffledCards = shuffling_algorithm.shuffle(originalCards)
		expectedOrder = [3,1,2]
		self.assertSequenceEqual(shuffledCards, expectedOrder)

	def test_3_part_shuffle_divisible_by_3_repeated(self):
		originalCards = [1,2,3];

		_repeated_twice(self, originalCards, DivideAndOverShuffle())

	def test_3_part_shuffle_not_divisible_by_3(self):
		originalCards = [1,2,3,4];

		shuffling_algorithm = DivideAndOverShuffle()
		shuffledCards = shuffling_algorithm.shuffle(originalCards)
		expectedOrder = [3,1,4,2]
		self.assertSequenceEqual(shuffledCards, expectedOrder)

	def test_3_part_shuffle_not_divisible_by_3_repeated(self):
		originalCards = [1,2,3,4];

		_repeated_twice(self, originalCards, DivideAndOverShuffle())

class CutAndMergeShuffleTest(unittest.TestCase):
	def test_alternating_shuffle_even(self):
		originalCards = [1,2,3,4]
		
		shuffling_algorithm = CutAndMergeShuffle()
		shuffledCards = shuffling_algorithm.shuffle(originalCards)
		expectedOrder = [1,3,2,4]
		self.assertSequenceEqual(shuffledCards, expectedOrder)

	def test_alternating_shuffle_even_repeated(self):
		originalCards = [1,2,3,4]
		
		_repeated_twice(self, originalCards, CutAndMergeShuffle())

	def test_alternating_shuffle_odd(self):
		originalCards = [1,2,3,4,5]
		
		shuffling_algorithm = CutAndMergeShuffle()
		shuffledCards = shuffling_algorithm.shuffle(originalCards)
		expectedOrder = [1,3,2,4,5]
		self.assertSequenceEqual(shuffledCards, expectedOrder)

	def test_alternating_shuffle_even_repeated(self):
		originalCards = [1,2,3,4,5]
		
		_repeated_twice(self, originalCards, CutAndMergeShuffle())

