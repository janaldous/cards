from abc import ABC, abstractmethod
from cards import valid_suits, DeckFactory
from player import Player

class Game(ABC):
	def __init__(self, card_type, shuffle_strategy):
		self.deck = DeckFactory.factory(card_type)
		self.players = []
		self.deck = shuffle_strategy.shuffle(self.deck)

class Lucky9Game(Game):
	payout_lucky9 = 3/2
	payout_tie = 7

	def __init__(self, shuffle_strategy):
		super().__init__('lucky9', shuffle_strategy)
		self.dealer = Lucky9Dealer()
		self.current_player_id = 0

	'''
		deals to each player including the dealer
	'''
	def deal(self):
		for idx, lucky9player in enumerate(self.players):
			lucky9player.add_card(self.deck.pop(0))
			self.set_next_player()
		self.dealer.add_card(self.deck.pop(0))
		self.set_next_player()

	def deal_to_player(self, player_index):
		if (player_index != self.current_player_id):
			raise ValueError('Not players turn ' + str(self.current_player_id))
		elif (player_index == -1):
			self.dealer.add_card(self.deck.pop(0))
			self.set_next_player()
		else:
			lucky9_player = self.players[player_index]
			lucky9_player.add_card(self.deck.pop(0))
			if self.is_2_or_under(lucky9_player.player.cards_in_hand):
				lucky9_player.player.decrease_money(lucky9_player.lucky9_bet)
			self.set_next_player()

	def skip_player(self, player_index):
		self.set_next_player()

	def add_player(self, player, lucky9_bet, tie_bet=0):
		self.players.append(Lucky9Player(len(self.players), player, lucky9_bet, tie_bet))

	@staticmethod
	def get_lucky9_value(cards):
		total = 0
		for card in cards:
			total += card.card_value()
		return total % 10

	@staticmethod
	def is_lucky9(cards):
		return Lucky9Game.get_lucky9_value(cards) == 9

	@staticmethod
	def is_2_or_under(cards):
		return Lucky9Game.get_lucky9_value(cards) <= 2

	def is_tie_with_dealer(self, cards):
		temp = []
		for card in cards:
			temp.append(card.exact_value())

		for card in self.dealer.cards_in_hand:
			card_exact_value = card.exact_value()
			if card_exact_value in temp:
				temp.remove(card_exact_value)

		return len(temp) == 0

	def payout_winners(self):
		for lucky9player in self.players:
			if self.is_tie_with_dealer(lucky9player.player.cards_in_hand):
				lucky9player.player.increase_money(lucky9player.tie_bet * self.payout_tie)
			else:
				lucky9player.player.decrease_money(lucky9player.tie_bet)

			if self.is_lucky9(lucky9player.player.cards_in_hand):
				lucky9player.player.increase_money(lucky9player.lucky9_bet * self.payout_lucky9)
				lucky9player.player.add_win()
			else:
				lucky9player.player.decrease_money(lucky9player.lucky9_bet)
				lucky9player.player.add_loss()

	'''
		deals 2 cards per player including dealer
	'''
	def start_game(self):
		self.remove_not_eligible_players()
		if len(self.players) < 2:
			raise ValueError('not enough players')

		self.deal()
		self.deal()

	def remove_not_eligible_players(self):
		for lucky9player in self.players:
			if not lucky9player.player.is_eligible:
				self.players.remove(lucky9player)

	def set_next_player(self):
		self.current_player_id += 1
		if (self.current_player_id == len(self.players)):
			self.current_player_id = -1

	def get_current_player(self):
		if (self.current_player_id >= 0):
			return self.players[self.current_player_id].player
		else:
			return self.dealer

	def reveal_dealer_hidden_card(self):
		self.dealer.down_card.face_card_up()

	def end_game(self):
		for lucky9player in self.players:
			lucky9player.player.cards_in_hand = []

		self.dealer.cards_in_hand = []

class GameFactory:
	@staticmethod
	def factory(type, shuffle_strategy):
		if type == 'lucky9': return Lucky9Game(shuffle_strategy)
		else: raise ValueError('game not recognized')

class Lucky9Player:
	def __init__(self, player_index, player, lucky9_bet, tie_bet = 0):
		self.id = player_index
		self.player = player
		self.lucky9_bet = lucky9_bet
		self.tie_bet = tie_bet

	def add_card(self, card):
		if len(self.player.cards_in_hand)+1 > 3:
			raise ValueError('Player cannot have more than 3 cards')
		else:
			self.player.add_card(card)

class Lucky9Dealer:
	def __init__(self):
		self.cards_in_hand = []
		self.up_card = None
		self.down_card = None

	def add_card(self, card):
		if len(self.cards_in_hand) == 0:
			card.face_card_down()
			self.cards_in_hand.append(card)
			self.down_card = card
		elif len(self.cards_in_hand) == 1:
			self.cards_in_hand.append(card)
			self.up_card = card
		elif len(self.cards_in_hand) == 2:
			self.cards_in_hand.append(card)
		else:
			raise ValueError('dealer cannot have more than 2 cards ' + str(self.cards_in_hand))

	def handle_move(self):
		return self.up_card.value < 5

class Lucky9PayoutCalculator:
	payout_lucky9 = 3/2
	payout_tie = 7

	def _is_lucky_9(self, cards):
		return (self._get_total_value(cards) == 9
			and all(card.card_value() in range(1, 10) for card in cards))

	def _is_total_9(self, cards):
		return self._get_total_value(cards) == 9

	def _is_2_3_4(self, cards):
		return sorted([c.value for c in cards]) == list(range(2,5))

	def _is_suited(self, cards):
		return all(card.suit == cards[0].suit for card in cards)

	def _get_total_value(self, cards):
		return sum([card.card_value() for card in cards])%10

	def calculate_bonus_winning(self, dealer_up_card, player_cards):
		if (dealer_up_card == None or len(player_cards) != 2):
			raise ValueError('dealer up card is empty or player cards is not enough')

		all_cards = [dealer_up_card, player_cards[0], player_cards[1]]

		if (self._is_total_9(all_cards)):
			if (self._is_2_3_4(all_cards)):
				if (self._is_suited(all_cards)):
					return 100
				else:
					return 40
			elif (all(card.value == 3 for card in all_cards)):
				if (self._is_suited(all_cards)):
					return 200
				else:
					return 50
			else:
				if (self._is_suited(all_cards)):
					return 30
				else:
					return 5

		return 0

	def calculate_tie_winning(self, dealer_cards, player_cards):
		if (len(dealer_cards) != 3 or len(player_cards) != 3):
			raise ValueError('dealer or player\'s cards is not enough')

		if (self._get_total_value(dealer_cards) == self._get_total_value(player_cards)):
			return self.payout_tie

		return 0

	def calculate_bet_winning(self, dealer_cards, player_cards):
		if (len(dealer_cards) != 3 or len(player_cards) != 3):
			raise ValueError('dealer or player\'s cards is not enough')

		if (self._get_total_value(dealer_cards) < self._get_total_value(player_cards)
			or (self._get_total_value(dealer_cards) == self._get_total_value(player_cards)
				and self._is_lucky_9(player_cards))):
			return self.payout_lucky9

		return 0
