from abc import ABC, abstractmethod
import random

class ShufflingStrategyAbstract(ABC):
      @abstractmethod
      def _shuffle_main(self, cards):
            pass

      def shuffle(self, cards, m = 1):
            for i in range(m):
                  cards = self._shuffle_main(cards)
            return cards


class RandomShuffle(ShufflingStrategyAbstract):
      def _shuffle_main(self, cards):
            random.shuffle(cards)
            return cards

class DivideAndOverShuffle(ShufflingStrategyAbstract):
      def _chunkify(self, lst, n):
            return [lst[i::n] for i in range(n)]

      def _shuffle_main(self, cards):
            temp = self._chunkify(cards, 3)
            cards = temp[2] + temp[0] + temp[1]
            return cards
            

class CutAndMergeShuffle(ShufflingStrategyAbstract):
      def _shuffle_main(self, cards):
            halfwayPoint = int(len(cards)/2)
            half1 = cards[0:halfwayPoint]
            half2 = cards[halfwayPoint:len(cards)]
            
            cards = []
            for i in range(halfwayPoint):
                  cards.append(half1[i])
                  cards.append(half2[i])
            if (len(cards)%2 == 1):
                  cards.append(half2[len(half2)-1])
            return cards