from __future__ import division
from time import sleep
import random
import itertools

#Define globals for cards.
SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10, 'A':11}
DECK = list('_'.join(card) for card in itertools.product(SUITS, RANKS))

#Define a list containing all ACEs.
ACE = list('_'.join(card) for card in itertools.product(SUITS, 'A'))
 
#Initialize chips a player should possess.
player_balance = 100.0

#Game class includes variable of 1 Deck and dealcard method. A Game is bound to 1 deck of card.
#Deck will be re-initialized (shuffled) when the game starts over.
class Game(object):   
    def __init__(self, adeck):
        self.adeck = adeck

    def dealcard(self, num):
        card = random.sample(self.adeck, num)
        self.adeck = [x for x in self.adeck if x not in card]
        return card

#Calculate the total value of a card list.
def calculate(alist):
    value = 0
    if len(alist) == 2 and len(set(alist)&set(ACE)) == 2:
        value = 12
    else:
        for i in range(len(alist)):
            value = value + VALUES[str(alist[i])[-1]]
    return value

#Determine if the player gets BlackJack.
def isBlackJack(alist):
    if len(alist) == 2 and calculate(alist) == 21:
        return True
    else:
        return False

#Perform Hit action.
def hit(hand, value, newcard):
    hand = hand + newcard
    value = calculate(hand)
    print hand
    if not set(hand).isdisjoint(ACE) and value > 21:
        for i in range(len(set(hand)&set(ACE))):              
            value -= 10
            if value <= 21:
                break
    print value
    if value > 21:
        value = 0
        print "Bust!"
    return hand, value

#Perform Stand action.
def stand(hand, value):
    value = calculate(hand)
    print hand
    print value
    return value

#Perform DoubleDown action.
def doubledown(hand, value, newcard, bet, balance):
    balance -= bet
    bet *= 2
    print "You have doubled bet. Now you have %.1f chips." %balance
    temp = hit(hand, value, newcard)
    return temp, bet, balance

#Perform Surrender action.
def surrender(bet, balance):
    balance += bet/2
    print "You have surrendered. You have %.1f chips." %balance, '\n'
    return balance

#This is the main function, doing things necessary to complete the whole game,
#such as betting, dealing, hitting, standing, doubledown, split, surrender
#for the player and hitting for the dealer, and displaying final results.
def startgame():
    
    deck = DECK
    dealer_hand = []
    dealer_value = 0
    player_hand = []
    player_value = 0
    player_bet = 0
    global player_balance
    player_1_2_hand = []
    player_1_2_value = []
    
    while True:
        s = raw_input("Please bet. The minimal bet allowed is 1 chip: ")
        try:
            player_bet = int(s)
        except ValueError:
            print "You need enter an integer."
            continue
        if player_bet not in range(1, int(player_balance + 1)):    
            print "You need enter proper amount. (no more than", int(player_balance), "chips)"
        else:
            player_balance = player_balance - player_bet
            print "You have", player_balance, "chips remained."
            break

#So far both player_balance and player_bet are initialized.
 
    game = Game(deck)
 
    for i in range(2):
        dealt_card = game.dealcard(2)       
        player_hand.append(dealt_card[0])
        dealer_hand.append(dealt_card[1])

    print "Dealer:"
    print "['" + dealer_hand[0] + "', 'UNKNOWN']"
    print "Player:"
    print player_hand
    
#So far both hands (dealer/player) are initialized but their values are not yet.
    
    while True:
        
        s = raw_input("Hit, Stand, DoubleDown, Split or Surrender? (h/s/d/p/u) ")
        
        if s == 'h':
            player_value = calculate(player_hand)
            while True:                
                t = raw_input("Are you sure to Hit? (y/n) ")
                if t == 'y':
                    temp = hit(player_hand, player_value, game.dealcard(1))
                    player_hand = temp[0]
                    player_value = temp[1]
                    if player_value == 0:
                        break
                elif t == 'n':
                    break
                else:
                    print "I am sorry, please enter y or n."
            break

        elif s == 's':
            player_value = stand(player_hand, player_value)
            break
        
        elif s == 'd':			
            if player_balance - player_bet >= 0:
                temp = doubledown(player_hand, player_value, game.dealcard(1), player_bet, player_balance)
                player_hand = temp[0][0]
                player_value = temp[0][1]
                player_bet = temp[1]
                player_balance = temp[2]
                break
            else:
                print "You don't have enough chips to double det, please select other option."
                continue

        elif s == 'p':
            if VALUES[str(player_hand[0])[-1]] == VALUES[str(player_hand[1])[-1]] and player_balance >= player_bet:
                player_balance -= player_bet
                print "Split means your bet doubled. Your new balance is %.1f chips." %player_balance
                p1 = []
                p2 = []
                p1 = player_hand + game.dealcard(1)
                p1.pop(1)
                p2 = player_hand + game.dealcard(1)
                p2.pop(0)
                player_1_2_hand = [p1, p2]
                player_1_2_value = [calculate(player_1_2_hand[0]), calculate(player_1_2_hand[1])]
                
                for i in range(len(player_1_2_hand)):
                    print "Split hand %d:" %(i + 1)
                    print player_1_2_hand[i]
                    print player_1_2_value[i]
                    while player_1_2_value[i] > 0:
                        p = raw_input("Do you want to Hit? (y/n) ")
                        if p == 'y':
                            temp = hit(player_1_2_hand[i], player_1_2_value[i], game.dealcard(1))
                            player_1_2_hand[i] = temp[0]
                            player_1_2_value[i] = temp[1]
                        elif p == 'n':
                            break
                        else:
                            print "I am sorry, please enter y or n."
                break
           
            else:
                print "You are not eligible to Split, please select other option."
                continue

        elif s == 'u':
            player_balance = surrender(player_bet, player_balance)
            return
            
        else:
            print "I am sorry, please enter h, s, d, p or u."

#Dealer starts to act from here.
    if player_value > 0 or player_1_2_value > [0, 0]:
        print
        print "Now it's dealer's turn..."
        print dealer_hand       
        dealer_value = calculate(dealer_hand)       
        print dealer_value  
        while 0 < dealer_value < 17:
                print "Dealer is hitting..."
                sleep(3)
                temp = hit(dealer_hand, dealer_value, game.dealcard(1))
                dealer_hand = temp[0]
                dealer_value = temp[1]
    print

#Display the final results.
    if player_1_2_value != []:
        for i in range(len(player_1_2_value)):
            print "Split hand", i + 1,
            if player_1_2_value[i] > dealer_value:
                player_balance += 2*player_bet
                print "wins.",
            elif player_1_2_value[i] !=0 and player_1_2_value[i] == dealer_value:
                player_balance += player_bet
                print "gets Push.",
            else:
                print "loses.",
        print "You have %.1f chips." %player_balance, '\n'
    
    else:        
        if player_value > dealer_value:
            if isBlackJack(player_hand):
                player_balance += 2.5*player_bet
                print "Congratulations. You get a BlackJack payout of 3:2. You have %.1f chips." %player_balance
            else:
                player_balance += 2*player_bet
                print "You win. You have %.1f chips." %player_balance
        elif player_value !=0 and player_value == dealer_value:
            player_balance += player_bet
            print "Push. You neither lose nor make money. You have %.1f chips." %player_balance
        else:
            print "You lose. You have %.1f chips." %player_balance    
        print
    
    return

if __name__ == "__main__":

    print '''Welcome to Yuqing's Casino! Here is my BlackJack rule:
    1. If you win with a BlackJack, bet payout is 3:2.
    2. You can surrender but half bet will be taken.
    3. You can select DoubleDown, only 1 more card will be hit, and
    bet will be doubled.
    4. Once Split, Re-split or Doubledown or Surrender is NOT allowed. 
    5. ACE by default is 11. If your 1st 2 cards are ACEs, your point
    is 12. If you choose Hit, and your point becomes > 21, then any
    ACE could be reduced to 1 so that your point is less than but close
    to 21.
    6. Dealer must hit if his point is < 17 (even if his point might >
    yours) and must stand if it is >= 17.
    '''
    
    while True:
        decision = raw_input("Start a new game? (y/n) ")
        if decision == 'y':
            if player_balance >= 1:
                startgame()
            else:
                print "You have less than 1 chip left. You can not afford minimal bet. Good-bye!"
                break
        elif decision == 'n':
            print "See you next time!"
            break
        else:
            print "I am sorry, please enter y or n."
