'''
      games: pusoy dos, blackjack
      shuffling: 3 parts, random shuffling, alternating
      player: agressive, passive, ?
'''

valid_suits = ['club', 'spade', 'heart', 'diamond']

class Card:
      suit_value = {
            'diamond': 3,
            'heart': 2, 
            'spade': 1, 
            'club': 0
      }
      min_value = 1
      max_value = 13

      def __init__(self, suit, value):
            if (suit not in valid_suits):
                  raise ValueError('Invalid suit, must be one of ' + str(valid_suits))

            if (value not in range(self.min_value, self.max_value+1)):
                  raise ValueError('Invalid value, must be within 1 to 13')

            self.suit = suit
            self.value = value
            self.face_down = False

      def exact_value(self):
            return self.value+(self.suit_value[self.suit]*self.max_value)

      def card_value(self):
            return self.exact_value()

      def compare_exact(self, card):
            return self.exact_value() - card.exact_value()

      def face_card_down(self):
            self.face_down = True

      def face_card_up(self):
            self.face_down = False

      def __str__(self):
            if not self.face_down:
                  return "{ suit: " + self.suit + ", value: " + str(self.value) + " }"
            else:
                  return "{ faced down }"

      def __repr__(self):
            return self.__str__()

class Lucky9Card(Card):
      def card_value(self):
            if (self.value in range(10, self.max_value+1)):
                  return 10

            return self.value

      def compare_game_value(self):
            return self.card_value() - card.card_value()

class CardFactory:
      def factory(type, suit, value):
            if type == 'lucky9': 
                  return Lucky9Card(suit, value)
            else: 
                  return Card(suit, value)

      factory = staticmethod(factory)

class DeckFactory:
      @staticmethod
      def deck(card_type):
            cards = []
            for suit in valid_suits:
                  for i in range(Card.min_value, Card.max_value+1):
                        cards.append(card_type(suit, i))
            return cards

      @staticmethod
      def factory(type):
            if type == 'lucky9': 
                  return DeckFactory.deck(Lucky9Card)
            else: 
                  return DeckFactory.deck(Card)
