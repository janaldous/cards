import unittest
from game import Lucky9Game, Lucky9Dealer, Lucky9Player
from player import Player, PlayerStrategy
from shuffle import RandomShuffle
from cards import Lucky9Card

class MockStrategy(PlayerStrategy):
	def pick_card(self):
		return true

class MockShuffle:
	def shuffle(self, cards):
		return cards

class Lucky9GameTest(unittest.TestCase):
	def test_create_lucky9_game(self):
		game = Lucky9Game(MockShuffle())
		player = Player(200, MockStrategy())

		game.add_player(player, 50)

		self.assertEqual(52, len(game.deck))
		self.assertEqual(1, len(game.players))

	def test_start_lucky9_game(self):
		game = Lucky9Game(MockShuffle())
		player = Player(200, MockStrategy())

		game.add_player(player, 50)
		game.add_player(Player(200, MockStrategy()), 50)

		game.start_game()

		self.assertEqual(2, len(player.cards_in_hand))

	def test_start_lucky9_game_not_enough_players(self):
		game = Lucky9Game(MockShuffle())
		player = Player(200, MockStrategy())

		self.assertRaises(ValueError, game.start_game)

	def test_is_lucky9(self):
		card1 = Lucky9Card('spade', 1)
		card2 = Lucky9Card('spade', 7)
		card3 = Lucky9Card('spade', 1)

		cards_in_hand = [card1, card2, card3]
		self.assertTrue(Lucky9Game.is_lucky9(cards_in_hand))

	def test_is_lucky9_10(self):
		card1 = Lucky9Card('spade', 2)
		card2 = Lucky9Card('spade', 7)
		card3 = Lucky9Card('spade', 10)

		cards_in_hand = [card1, card2, card3]
		self.assertTrue(Lucky9Game.is_lucky9(cards_in_hand))

	def test_is_not_lucky9_10(self):
		card1 = Lucky9Card('spade', 3)
		card2 = Lucky9Card('spade', 7)
		card3 = Lucky9Card('spade', 10)

		cards_in_hand = [card1, card2, card3]
		self.assertFalse(Lucky9Game.is_lucky9(cards_in_hand))

	def test_payout_player_lucky9_win(self):
		game = Lucky9Game(MockShuffle())
		card1 = Lucky9Card('spade', 2)
		card2 = Lucky9Card('spade', 7)
		card3 = Lucky9Card('spade', 10)

		cards_in_hand = [card1, card2, card3]
		player = Player(200, MockStrategy())
		game.add_player(player, 50)
		player.cards_in_hand = cards_in_hand

		game.payout_player(0)
		self.assertEqual(275, player.money)

	def test_payout_player_lucky9_lose(self):
		game = Lucky9Game(MockShuffle())
		card1 = Lucky9Card('spade', 3)
		card2 = Lucky9Card('spade', 7)
		card3 = Lucky9Card('spade', 10)

		cards_in_hand = [card1, card2, card3]
		player = Player(200, MockStrategy())
		game.add_player(player, 50)
		player.cards_in_hand = cards_in_hand

		game.payout_player(0)
		self.assertEqual(150, player.money)

	def test_is_tie_with_dealer(self):
		game = Lucky9Game(MockShuffle())
		player_card1 = Lucky9Card('spade', 2)
		player_card2 = Lucky9Card('spade', 7)
		player_card3 = Lucky9Card('spade', 10)

		dealer_card1 = Lucky9Card('spade', 2)
		dealer_card2 = Lucky9Card('spade', 7)
		dealer_card3 = Lucky9Card('spade', 10)

		player_cards_in_hand = [player_card2, player_card1, player_card3]
		dealer_cards_in_hand = [dealer_card1, dealer_card3, dealer_card2]
		
		game.dealer.cards_in_hand = dealer_cards_in_hand

		self.assertTrue(game.is_tie_with_dealer(player_cards_in_hand))

	def test_is_not_tie_with_dealer(self):
		game = Lucky9Game(MockShuffle())
		player_card1 = Lucky9Card('spade', 2)
		player_card2 = Lucky9Card('spade', 7)
		player_card3 = Lucky9Card('spade', 10)

		dealer_card1 = Lucky9Card('spade', 3)
		dealer_card2 = Lucky9Card('spade', 7)
		dealer_card3 = Lucky9Card('spade', 10)

		player_cards_in_hand = [player_card2, player_card1, player_card3]
		dealer_cards_in_hand = [dealer_card1, dealer_card3, dealer_card2]
		
		game.dealer.cards_in_hand = dealer_cards_in_hand

		self.assertFalse(game.is_tie_with_dealer(player_cards_in_hand))

	def test_deal_to_player_3_cards(self):
		game = Lucky9Game(MockShuffle())
		player = Player(200, MockStrategy())
		game.add_player(player, 50)
		self.assertEqual(1, len(game.players))
		game.deal()
		game.deal()
		game.deal_to_player(0)
		self.assertEqual(3, len(player.cards_in_hand))

	def test_deal_to_player_4_cards(self):
		game = Lucky9Game(MockShuffle())
		player = Player(200, MockStrategy())
		game.add_player(player, 50)
		game.deal()
		game.deal()
		game.deal_to_player(0)
		game.deal_to_player(-1)
		self.assertEqual(3, len(player.cards_in_hand))

		self.assertRaises(ValueError, game.deal_to_player, 0)

class Lucky9PlayerTest(unittest.TestCase):
	def test_add_player(self):
		game = Lucky9Game(MockShuffle())
		player1 = Player(200, MockStrategy())
		player2 = Player(200, MockStrategy())
		game.add_player(player1, 50)
		self.assertEqual(0, game.players[0].id)
		game.add_player(player2, 50)
		self.assertEqual(1, game.players[1].id)

class Lucky9DealerTest(unittest.TestCase):
	def test_lucky9_dealer(self):
		dealer = Lucky9Dealer()
		dealer.add_card(Lucky9Card('spade', 1))
		self.assertIsNotNone(dealer.down_card)

		dealer.add_card(Lucky9Card('spade', 2))
		self.assertIsNotNone(dealer.up_card)

		dealer.add_card(Lucky9Card('spade', 4))

		self.assertRaises(ValueError, dealer.add_card, Lucky9Card('spade', 3))

	def test_pick_card_lower_boundary(self):
		dealer = Lucky9Dealer()
		dealer.up_card = Lucky9Card('spade', 4)

		self.assertTrue(dealer.pick_card())

	def test_pick_card_on_boundary(self):
		dealer = Lucky9Dealer()
		dealer.up_card = Lucky9Card('spade', 5)

		self.assertFalse(dealer.pick_card())

	def test_pick_card_upper_boundary(self):
		dealer = Lucky9Dealer()
		dealer.up_card = Lucky9Card('spade', 6)

		self.assertFalse(dealer.pick_card())