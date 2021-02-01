### the card game war
import random

suits =  ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks =  ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9, 'Ten':10, 'Jack':11, 'Queen':11, 'King':11, 'Ace':11}

class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank] #converts string to int

    def __repr__(self):
        return self.rank + ' of ' + self.suit

class Deck():

    def __init__(self):

        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Player():

    def __init__(self,name):
        self.name = name
        self.hand = []

    def hit_me(self):
        return self.hand.append(game_deck.deal_one())

    def hand_value(self):
        hand_val = 0
        for cards in self.hand:
            hand_val += values[cards.rank]
            return hand_val

game_deck = Deck()
game_deck.shuffle()

rob = Player('rob')

rob.hit_me()

print('{} has {}'.format(rob.name,rob.hand_value()))
print(game_deck.all_cards)
