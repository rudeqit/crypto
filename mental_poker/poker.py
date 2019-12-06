#!/usr/bin/env python3

# Питон говно короче (как и этот код) :(

# Add path to our lib
import random
import sys
sys.path.append("..")

from operations.operations import pow_mod, get_g_p, get_mut_prime, get_rand_simple
from ciphers.shamir import Subscriber

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Пошаговый режим
STEP_BY_STEP = True

class Card:
    '''
    Класс для представляния одной карты. 
    Содержит поля suit(масть) и rank(значение)
    Suit и rank инициализируются строками,
    но в процессе (при кодировании) кастуются в list,
    где каждый элемент list'a - это символ числа в utf кодировке.
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

    def to_lists(self):
        list_suit = []
        list_rank = []
        
        for elem in self.suit:
            list_suit.append(ord(elem))

        for elem in self.rank:
            list_rank.append(ord(elem))

        return list_suit, list_rank

    def list_to_str(self):
        _suit = ""
        _rank = ""

        for elem in self.suit:
            _suit += chr((elem))
        
        for elem in self.rank:
            _rank += chr((elem))

        self.suit, self.rank = _suit, _rank

class Deck:
    '''
    Класс колоды. Содержит, собственно, саму колоду и методы для неё.
    '''

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return deck_comp

    def cards(self):
        return self.deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Player:
    '''
    Класс игрока. Хранит секретные ключи c и d.
    Число p общее на всю сессию, его задает диллер.
    У игрока есть рука и методы для кодирования/декодирования карты.  
    '''

    # Статическая переменная, инкрементируется при вызове конструктора
    player_counter = 0

    def __init__(self, p):
        self.__class__.player_counter += 1
        self.id = self.__class__.player_counter
        
        self.shamir = Subscriber(p)
        
        self.c = self.shamir.c
        self.d = self.shamir.d

        self.hand = []

    def encode(self, card: Card) -> tuple:
        list_suit, list_rank = [], []

        if (type(card.suit) == str): 
            list_suit, list_rank = card.to_lists()
        elif (type(card.suit) == list):
            list_suit, list_rank = card.suit, card.rank
        else:
            raise ValueError(f"card.suit and card.rank have type {type(card.suit)}")
        
        _list_suit, _list_rank = [], []
        for elem in list_suit:
            _list_suit.append(self.shamir.encode(elem))

        for elem in list_rank:
            _list_rank.append(self.shamir.encode(elem))

        card.suit, card.rank = _list_suit, _list_rank
        return _list_suit, _list_rank

    def decode(self, card: Card) -> tuple:
        suit, rank = self.decode_to_list(card.suit, card.rank)
        card.suit, card.rank = suit, rank
        return suit, rank

    def decode_to_list(self, suit: list, rank: list) -> tuple:
        _suit, _rank = [], []

        for elem in suit:
            _suit.append(self.shamir.decode(elem))

        for elem in rank:
            _rank.append(self.shamir.decode(elem))
        
        return _suit, _rank

    def decode_by_yourself(self, card: Card) -> str:
        self.decode(card)
        card.list_to_str()
        return str(card)

class Dealer:
    """
    Инициализирует и хранит колоду, задает число p
    Может просить игроков кодировать/декодировать карту,
    выкладывать карты на стол и раздавать их.
    """
    
    def __init__(self):
        self.deck = Deck()
        self.p = get_rand_simple()

    # Кодирование одной карты
    def encode_card(self, card, players):
        for player in players:
            player.encode(card)

    # Кодирование всей колоды
    def encode_cards(self, players):
        for card in self.deck.cards():
            self.encode_card(card, players)

    # Декоирование одной карты 
    def _decode_card(self, card, player):
        return player.decode(card)

    # Декоирование одной карты всеми игроками 
    def decode_card(self, card, players) -> str:
        for player in players:
            player.decode(card)
        card.list_to_str()
        return card

    # Раздаем по две карты игрокам
    def deal(self, players):
        self.deck.shuffle()
        
        for i in range(0, 2):
            for player in players:
                card = self.deck.deal()
                for pl in players:
                    if pl == player: continue
                    self._decode_card(card, pl)
                player.hand.append(card)
        
        self.deck.shuffle()

    # Карту на стол!
    def card_on_table(self, players):
        encode_card = self.deck.deal()
        return self.decode_card(encode_card, players)
        

class Poker:
    """
    Схема игры: Диллер в самом начале пускает колоду по игрокам
    с целью шифрования. После, диллер раздает игрокам карты, прося
    при этом всех игроков, кроме будущего обладателя карты, расшифровать
    ее своим ключом. Теперь владелец карты, применив свой ключ, может 
    узнать свою карту. Дальше на стол выкладываются карты для комбинаций,
    по той же схеме, что и при раздаче, только теперь абсолютно все 
    применяют свои ключи. И в конце игроки открывают свои карты, применяя публично
    свой секретный ключ.
    """

    def __init__(self, players_num):
        if players_num < 2 or players_num > 23:
            raise ValueError(f"Oops, i cant's start game with {players_num} players!"
                             " Min number of players is 2,"
                             " Max is 23.")

        self.dealer = Dealer()

        # Стол, на котором будут лежать 5 карт 
        # сначала три - флоп, еще одна - терн, и последняя - ривер
        self.table = []

        self.players = []
        for i in range(0, players_num):
            self.players.append(Player(self.dealer.p))
            
    # Три карты на столе (начало)
    def flop(self):
        for i in range(0, 3):
            card = self.dealer.card_on_table(self.players)
            self.table.append(card)

    # Четыре карты на столе
    def tern(self):
        card = self.dealer.card_on_table(self.players)
        self.table.append(card)

    # Пять карт на столе (конец)
    def river(self):
        card = self.dealer.card_on_table(self.players)
        self.table.append(card)
    
    def show(self, Message):
        print(f"{Message}\n")
        print("------------------------------------------\n")
        print("Table:")
        for card in self.table:
            print(f"\t{str(card)}")

        print()

        for player in self.players:
            print(f"Player {player.id} and his hand:")
            for card in player.hand:
                print(f"\t{card.suit} of {card.rank}")
            print()
        print("------------------------------------------")

    def open_cards(self):
        for player in self.players:
            for card in player.hand:
                player.decode_by_yourself(card)

    def game(self):
        self.dealer.encode_cards(self.players)
        self.show("Init, table is empthy")

        if STEP_BY_STEP:
            input()

        self.dealer.deal(self.players)
        self.show("Give card to players")

        if STEP_BY_STEP:
            input()

        self.flop()
        self.tern()
        self.river()
    
        self.show("Flop, tern, river")
        if STEP_BY_STEP:
            input()

        self.open_cards()
        self.show("Decode their card")
        

if __name__ == "__main__":
    poker = Poker(2)
    poker.game()