#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
class Suit:
    def __init__( self, name, symbol ):
        self.name = name
        self.symbol = symbol
    def __str__(self):
        return self.symbol
    
class Card:
    def __init__( self, rank, suit, hard, soft ):
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft
    def __str__(self):
        return '{}{}'.format(self.rank, self.suit)
        
class NumberCard(Card):
    def __init__( self, rank, suit ):
        super().__init__( str(rank), suit, rank, rank )
    
class AceCard(Card):
    def __init__( self, rank, suit ):
        super().__init__( "A", suit, 1, 11 )
    
class FaceCard(Card):
    def __init__( self, rank, suit ):
        super().__init__( {11: 'J', 12: 'Q', 13: 'K' }[rank], suit,10, 10 )
    
def card( rank, suit ):
    if rank == 1: return AceCard(rank, suit)
    elif 2 <= rank < 11: return NumberCard(rank, suit)
    elif 11 <= rank < 14: return FaceCard(rank, suit)
    else:
        raise Exception( "Rank out of range" )

Club, Diamond = Suit('Club','♣'), Suit('Diamond','♦')
Heart,  Spade = Suit('Heart','♥'), Suit('Spade','♠')

class Deck(list):
    def __init__(self):
        super().__init__( card(r+1,s) for r in range(13) for s in (Club, Diamond, Heart, Spade) )
        random.shuffle(self)
    def __str__(self):
        for i in self:
            return str(i)
        
d = Deck()
hand = [ d.pop(), d.pop() ]
print(len(d))
for i in hand:
    print(i)
