import unittest
from player import StreakyStrategy, StrategicStrategy



class StreakyStrategyTest(unittest.TestCase):
	def test_won_once_only(self):
		strategy = StreakyStrategy()

		self.assertEqual(False, strategy.pick_card(1))

	def test_won_thrice(self):
		strategy = StreakyStrategy()

		self.assertEqual(True, strategy.pick_card(3))

class StrategyStrategyTest(unittest.TestCase):
	def test_probability_less_than_half(self):
		strategy = StrategicStrategy()
		self.assertEqual(False, strategy.pick_card(0.49))

	def test_probability_is_half(self):
		strategy = StrategicStrategy()
		self.assertEqual(False, strategy.pick_card(0.5))

	def test_probability_more_than_half(self):
		strategy = StrategicStrategy()
		self.assertEqual(True, strategy.pick_card(0.501))