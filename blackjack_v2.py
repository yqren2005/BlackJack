import random

SUITS = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
MAX_PLAYERS = 8
MAX_BALANCE = 1000
chip_balance = 0


class Card(object):

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if rank == 'A':
            self.point = 11
        elif rank in ['K', 'Q', 'J']:
            self.point = 10
        else:
            self.point = int(rank)

        self.is_hidden = False
        self.is_ace = True if self.rank == 'A' else False

    def __str__(self):
        if self.is_hidden:
            return '[X]'
        else:
            return '[' + self.suit + ' ' + self.rank + ']'

    def hide_card(self):
        self.is_hidden = True

    def reveal_card(self):
        self.is_hidden = False


class Deck(object):

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)


class Hand(object):

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        return self.cards

    def get_value(self):
        value = sum(card.point for card in self.cards)
        aces = sum(card.is_ace for card in self.cards)
        while (value > 21) and aces:
            value -= 10
            aces -= 1
        return value


class Dealer(object):

    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand()
        self.is_bust = False

    def show_hand(self):
        for card in self.hand.cards:
            print card,
        print

    def hit(self):
        print "Hitting..."
        self.hand.add_card(self.deck.deal_card())
        return self.hand.cards

    def stand(self):
        print "%s gets %d. Done." % (self.name, self.hand.get_value())

    def check_bust(self):
        if self.hand.get_value() > 21:
            self.is_bust = True
            print "%s gets bust!" % self.name
        else:
            self.stand()


class Player(Dealer):

    def __init__(self, name, deck, bet):
        Dealer.__init__(self, name, deck)
        self.bet = bet
        self.is_surrender = False
        self.is_split = False
        self.split = []


def play(player, deck):
    print player.name + ':',
    player.show_hand()
    if player.name == 'Dealer':
        while player.hand.get_value() < 17:
            player.hit()
            player.show_hand()
        player.check_bust()
    else:
        global chip_balance
        if chip_balance >= player.bet and not player.is_split:
            if player.hand.cards[0].point == player.hand.cards[1].point:
                choice = input_func("Hit, Stand, DoubleDown, Split or Surrender? (h/s/d/p/u) ", str.lower,
                                    range_=('h', 's', 'd', 'p', 'u'))
            else:
                choice = input_func("Hit, Stand, DoubleDown or Surrender? (h/s/d/u) ", str.lower,
                                    range_=('h', 's', 'd', 'u'))
        else:
            choice = input_func(
                "Hit, Stand or Surrender? (h/s/u) ", str.lower, range_=('h', 's', 'u'))
        while choice == 'h':
            player.hit()
            player.show_hand()
            if player.hand.get_value() > 21:
                player.is_bust = True
                print "%s gets bust!" % player.name
                break
            choice = input_func(
                "Hit or Stand? (h/s) ", str.lower, range_=('h', 's'))

        if choice == 's':
            player.stand()

        if choice == 'd':
            chip_balance -= player.bet
            print "New balance = %d" % chip_balance
            player.bet *= 2
            player.hit()
            player.show_hand()
            player.check_bust()

        if choice == 'u':
            chip_balance += (player.bet - player.bet / 2)
            print "New balance = %d" % chip_balance
            player.is_surrender = True

        if choice == 'p':
            chip_balance -= player.bet
            print "New balance = %d" % chip_balance
            player.split.append(Player(' Split_1', deck, player.bet))
            player.split.append(Player(' Split_2', deck, player.bet))
            for p in player.split:
                p.hand.add_card(player.hand.cards.pop(0))
                p.hand.add_card(deck.deal_card())
                p.is_split = True
                play(p, deck)


def input_func(prompt, type_=None, min_=None, max_=None, range_=None):
    value = ''
    while True:
        value = raw_input(prompt)
        if type_ is not None:
            try:
                value = type_(value)
            except ValueError:
                print "Sorry I don't understand."
                continue
        if min_ is not None and value < min_:
            print "Sorry your input can not be less than %d!" % min_
        elif max_ is not None and value > max_:
            print "Sorry your input can not be more than %d!" % max_
        elif range_ is not None and value not in range_:
            print "You must select from", range_
        else:
            break
    return value


def award_winnings(player, dealer):
    global chip_balance
    if player.is_surrender:
        tag = 'surrender'
    elif player.is_bust:
        tag = 'lose'
    elif len(player.hand.cards) == 2 and player.hand.get_value() == 21 and not player.is_split:
        tag = 'blackjack'
        chip_balance += player.bet * 5 / 2
    elif dealer.is_bust or (player.hand.get_value() > dealer.hand.get_value()):
        tag = 'win'
        chip_balance += player.bet * 2
    elif player.hand.get_value() == dealer.hand.get_value():
        tag = 'push'
        chip_balance += player.bet
    else:
        tag = 'lose'
    print "%s: %-*s Balance = %d" % (player.name, 10, tag, chip_balance)


def game():
    players = []
    global chip_balance
    deck = Deck()

    player_num = input_func(
        "\nPlease enter the number of players: (1-8) ", int, 1, MAX_PLAYERS)

    print "\nLet's get started...\n"

    for i in range(player_num):
        if chip_balance > 0:
            player_name = 'Player_' + str(i + 1)
            print "%s:" % player_name
            player_bet = input_func(
                "Please bet. The minimal bet is 1 chip. ", int, 1, chip_balance)
            chip_balance -= player_bet
            print "Balance updated. New balance is %d." % chip_balance
            player = Player(player_name, deck, player_bet)
            players.append(player)
        else:
            print "\nThe actual number of player is %d. There's no balance to support more players." % (len(players))
            break

    dealer = Dealer('Dealer', deck)

    for i in range(2):
        for player in (players + [dealer]):
            player.hand.add_card(deck.deal_card())

    dealer.hand.cards[1].hide_card()
    print "\nDealer:"
    dealer.show_hand()
    print
    dealer.hand.cards[1].reveal_card()

    for player in (players + [dealer]):
        play(player, deck)
        print

    print "...Final result...\n"

    for player in players:
        if not player.split:
            award_winnings(player, dealer)
        else:
            print "%s: split" % player.name
            for p in player.split:
                award_winnings(p, dealer)

    print "\nFinal chip balance is %d.\n" % chip_balance


if __name__ == '__main__':

    chip_balance = input_func(
        "\nWelcome to BlackJack! Please enter the chip balance: (1-1000) ", int, 1, MAX_BALANCE)
    while True:
        game()
        if chip_balance < 1:
            print "You don't have enough balance to proceed. Game over."
            break
        proceed = input_func(
            "Do you want to continue? (y/n) ", str.lower, range_=('y', 'n'))
        if proceed == 'n':
            print "\nThank you for playing! See you next time."
            break
