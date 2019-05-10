from abc import ABC, abstractmethod
import random

class Player:
	def __init__(self, initial_money, player_strategy):
		self.money = initial_money
		self.strategy = player_strategy
		self.cards_in_hand = []
		self.wins = 0
		self.is_eligible = True

	def increase_money(self, income):
		self.money += income
		if self.money > 0: self.is_eligible = True

	def decrease_money(self, spend):
		self.money -= spend
		if self.money <= 0: self.is_eligible = False

	def add_card(self, card):
		self.cards_in_hand.append(card)

	def handle_move(self):
		return self.strategy.pick_card()

	def add_win(self):
		self.wins += 1

	def add_loss(self):
		self.wins -= 1

	def __str__(self):
		return 'Player({},{},{})'.format(self.money,
                                         self.cards_in_hand,
                                         self.wins)

class PlayerStrategy(ABC):
	'''
		returns true or false if should pick card
	'''
	@abstractmethod
	def pick_card(self):
		pass

class HumanStrategy(PlayerStrategy):
	def pick_card(self):
		pick = int(input("Enter [1] deal, [0] pass: "))
		return pick == 1

class RandomStrategy(PlayerStrategy):
	def pick_card(self):
		return random.randint(0,1)

class StreakyStrategy(PlayerStrategy):
	#ask_limit??

	def pick_card(self, games_won):
		return games_won >= 2

class StrategicStrategy(PlayerStrategy):
	#ask_limit??

	def pick_card(self, probability_increase_value):
		return probability_increase_value > 0.5