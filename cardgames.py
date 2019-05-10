'''
      games: pusoy dos, blackjack
'''
from abc import ABC, abstractmethod

class Game(ABC):
	self.deck = []
	self.players = []
	'''
    	starts a game
    '''
    def start_game(self, deck_factory):
    	print("getting new deck")
    	#get deck
    	self.deck = deck_factory.create_deck()
    	
    	#distribute cards
    	print("dealer is dealing cards")
    	for player, i in players, range(len(self.deck)):
    		player.add_card(self.deck.pop(i))
    	print("game is set, player 1 turn")
		
	@abstractmethod
    def select_players():
        pass

