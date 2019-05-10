from game import GameFactory
from shuffle import RandomShuffle
from player import Player, HumanStrategy, RandomStrategy


def print_cards(player):
	print(game.get_lucky9_value(player.cards_in_hand), player.cards_in_hand)

def print_player(player):
	print("player="+str(player))
	print("\tvalue=" + str(game.get_lucky9_value(player.cards_in_hand)))

def make_player_move(player):
	print("---------player " + str(player) + " is making a move")

	if player.handle_move():
		print("== DEAL")
		game.deal_to_player(game.current_player_id)
		if player == game.dealer: print_cards(player)
		else: print_player(player)
	else:
		print("== PASS")
		game.skip_player(game.current_player_id)
		print_cards(player)

	print("----------player move ends")

def print_all_players():
	print_player(player1)
	print_player(player2)
	print_cards(game.dealer)


shuffle_strategy = RandomShuffle()

game = GameFactory.factory('lucky9', shuffle_strategy)

initial_money = 200
player1 = Player(initial_money, HumanStrategy())
player2 = Player(initial_money, RandomStrategy())
player2 = Player(initial_money, RandomStrategy())

game.add_player(player1, 50)
game.add_player(player2, 50)


while len(game.deck) > 0:
	print("=====START GAME=======")
	game.start_game()

	print_player(player1)
	print_player(player2)

	make_player_move(game.get_current_player())

	make_player_move(game.get_current_player())

	make_player_move(game.get_current_player())

	print("--------paying out tie winners")
	game.reveal_dealer_hidden_card()
	game.payout_winners()

	print_all_players()
	game.end_game()
	print("=====END GAME=======")