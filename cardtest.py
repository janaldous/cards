import unittest
from cards import Card, Lucky9Card, valid_suits, CardFactory, DeckFactory

class CardTest(unittest.TestCase):
	def test_create_card_spade(self):
		suit = 'spade'
		value = 1
		card = Card(suit, value)

		self.assertEqual(suit, card.suit)
		self.assertEqual(value, card.value)

	def test_create_card_heart(self):
		suit = 'heart'
		value = 13
		card = Card(suit, value)

		self.assertEqual(suit, card.suit)
		self.assertEqual(value, card.value)

	def test_create_card_diamond(self):
		suit = 'diamond'
		value = 1
		card = Card(suit, value)

		self.assertEqual(suit, card.suit)
		self.assertEqual(value, card.value)

	def test_create_card_club(self):
		suit = 'club'
		value = 13
		card = Card(suit, value)

		self.assertEqual(suit, card.suit)
		self.assertEqual(value, card.value)

	def test_create_invalid_card_suit(self):
		suit = 'apple'
		value = 1

		self.assertRaises(ValueError, Card, suit, value)

	def test_create_invalid_card_value_lower_boundary(self):
		suit = 'spade'
		value = 0

		self.assertRaises(ValueError, Card, suit, value)

	def test_create_invalid_card_value_upper_boundary(self):
		suit = 'spade'
		value = 14

		self.assertRaises(ValueError, Card, suit, value)

	def test_compare_lower_value_same_suit(self):
		card1 = Card('spade', 1)
		card2 = Card('spade', 2)

		self.assertEqual(-1, card1.compare_exact(card2))

	def test_compare_higher_value_same_suit(self):
		card1 = Card('spade', 1)
		card2 = Card('spade', 2)

		self.assertEqual(1, card2.compare_exact(card1))

	def test_card_value(self):
		cardc1 = Card('club', 1)
		cardc2 = Card('club', 13)
		cards1 = Card('spade', 1)
		cards2 = Card('spade', 13)
		cardh1 = Card('heart', 1)
		cardh2 = Card('heart', 13)
		cardd1 = Card('diamond', 1)
		cardd2 = Card('diamond', 13)
		self.assertEqual(1, cardc1.card_value())
		self.assertEqual(13, cardc2.card_value())
		self.assertEqual(14, cards1.card_value())
		self.assertEqual(26, cards2.card_value())
		self.assertEqual(27, cardh1.card_value())
		self.assertEqual(39, cardh2.card_value())
		self.assertEqual(40, cardd1.card_value())
		self.assertEqual(52, cardd2.card_value())

class Lucky9CardTest(unittest.TestCase):
	def test_card_value(self):
		for suit in valid_suits:
			cardc1 = Lucky9Card(suit, 1)
			cardc2 = Lucky9Card(suit, 9)
			cardc3 = Lucky9Card(suit, 10)
			cardc4 = Lucky9Card(suit, 13)
			self.assertEqual(1, cardc1.card_value())
			self.assertEqual(9, cardc2.card_value())
			self.assertEqual(10, cardc3.card_value())
			self.assertEqual(10, cardc4.card_value())

	def test_to_string(self):
		card = Lucky9Card('spade', 1)
		self.assertEqual("{ suit: spade, value: 1 }", str(card))

class CardFactoryTest(unittest.TestCase):
	def test_card_factory_lucky9(self):
		lucky9_card = CardFactory.factory('lucky9', 'spade', 1)
		expected = Lucky9Card('spade', 1)

		self.assertEqual(expected.suit, lucky9_card.suit)
		self.assertEqual(expected.value, lucky9_card.value)

	def test_card_factory_default(self):
		lucky9_card = CardFactory.factory('', 'spade', 1)
		expected = Card('spade', 1)

		self.assertEqual(expected.suit, lucky9_card.suit)
		self.assertEqual(expected.value, lucky9_card.value)

class DeckFactoryTest(unittest.TestCase):
	def test_deck_factory_lucky9(self):
		deck = DeckFactory.factory('lucky9')
		self.assertEqual(52, len(deck))

	def test_deck_factory_default(self):
		deck = DeckFactory.factory('default')
		self.assertEqual(52, len(deck))