
# coding: utf-8

# In[1]:

# Used for card shuffle.
import random

# Boolean used to know if hand is in play.
playing = False

# Could also make this a raw input.
chip_pool = 100

bet = 1

restart_phrase = "Press 'd' to deal the cards again, or press 'q' to quit."


# In[2]:

# Hearts, Diamonds, Clubes, Spades
suits = ('H', 'D', 'C', 'S')

# Possible card ranks.
ranking = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')

# Point values dict.
card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}


# In[3]:

# Create a Card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def draw(self):
        print (self.suit + self.rank)


# In[4]:

# Create a Hand class
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        # Aces can be 1 or 11 so need to define it here
        self.ace = False
        
    def __str__(self):
        hand_comp = ""
        
        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name
            
        return "The hand has %s" % hand_comp
    
    def card_add(self, card):
        self.cards.append(card)
        
        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]
        
    def calc_val(self):
        
        if self.ace == True and self.value < 12:
            return self.value + 10
        else:
            return self.value
        
    def draw(self, hidden):
        if hidden == True and playing == True:
            starting_card = 1
        else:
            starting_card = 0
            
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()


# In[5]:

# Create the Deck class
class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit,rank))
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
    def __str__(self):
        deck_comp = ""
        for card in self.cards:
            deck_comp += " " + deck_comp.__str__()
            
        return "The deck has " + deck_comp


# In[6]:

# First Bet
def make_bet():
    global bet
    bet = 0
    
    print "What amount of chips would you like to bet? (Enter whole integer please)"
    
    # While loop to keep asking for the bet
    while bet == 0:
        # Use bet_comp as a checker
        bet_comp = raw_input()
        bet_comp = int(bet_comp)
        
        # Check to make sure the bet is within the remaining amount of chips left.
        if (bet_comp >= 1 and bet_comp <= chip_pool):
            bet = bet_comp
        else:
            print "Invalid bet, you only have " + str(chip_pool) + " remaining."


# In[7]:

# Function to setting up the game and for dealing out the cards.
def deal_cards():
    
    # Set up all global variables
    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet
    
    # Create a deck
    deck = Deck()
    
    # Shuffle it
    deck.shuffle()
    
    # Set up bet
    make_bet()
    
    # Set up both player and dealer hands
    player_hand = Hand()
    dealer_hand = Hand()
    
    # Deal out initial cards
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())
    
    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())
    
    result = "Hit or Stand? Press either 'h' or 's': "
    
    if playing:
        print "Fold, Sorry"
        chip_pool -= bet
        
    # Set up to know currently playing hand
    playing = True
    game_step()


# In[8]:

# Hit Function
def hit():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet
    
    if playing:
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())
            
        print "Player hand is %s" % player_hand
        
        if player_hand.calc_val() > 21:
            result = "Busted! " + restart_phrase
            
            chip_pool -= bet
            playing = False
            
    else:
        result = "Sorry, can't hit. " + restart_phrase
        
    game_step()


# In[9]:

# Stand Function
def stand():
    global playing,chip_pool,deck,player_hand,dealer_hand,result,bet
    
    if not playing:
        if player_hand.calc_val() > 0:
            result = "Sorry, you can't stand!"
            
    # Now go through all the other possible options
    else:
        
        # Soft 17 rule
        while dealer_hand.calc_val() < 17:
            dealer_hand.card_add(deck.deal())
            
        # Dealer Busts
        if dealer_hand.calc_val() > 21:
            result = "Dealer busts! You Win! " + restart_phrase
            chip_pool += bet
            playing = False
            
        # Player has better and than dealer
        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = "You beat the dealer, you win! " + restart_phrase
            chip_pool += bet
            playing = False
            
        # Push
        elif dealer_hand.calc_val() == player_hand.calc_val():
            result = "Tied up, push! " +  restart_phrase
            playing = False
            
        # Dealer beats Player
        else:
            result = "Dealer Wins! " + restart_phrase
            chip_pool -= bet
            playing = False
            
    game_step()


# In[10]:

# Function to print results and ask user for next step
def game_step():
    
    # Display Player Hand
    print ""
    print "Player Hand is: "
    player_hand.draw(hidden=False)
    
    print "Player Hnad total is: " + str(player_hand.calc_val())
    
    # Display Dealer Hnad
    print "Dealer Hand is: "
    dealer_hand.draw(hidden=True)
    
    # If game round is over
    if not playing:
        print " --- for a total of " + str(dealer_hand.calc_val())
        print "Chip Total: " + str(chip_pool)
        
    # Otherwise, don't know the second card yet
    else:
        print " with another card hidden upside down"
        
    # Print result of hit or stand
    print result
    
    player_input()


# In[11]:

# Function to exit the game
def game_exit():
    print "Thanks for playing!"
    exit()


# In[12]:

# Function to read user input
def player_input():
    plin = raw_input().lower()
    
    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin == 'd':
        deal_cards()
    elif plin == 'q':
        game_exit()
    else:
        print "Invalid Input...Enter h, s, d or q: "
        player_input()


# In[13]:

# Quick Intro Function
def intro():
    statement = '''Welcome to BlackJack! Get as close to 21 as you can without going over!
    Dealer hits until she reaches 17. Aces count as 1 or 11.
    Card output goes a letter followed by a number of face notation'''
    print statement


# In[ ]:

# Now to play the game!

#Create a Deck
deck = Deck()

#Shuffle it
deck.shuffle()

# Create player and dealer hands
player_hand = Hand()
dealer_hand = Hand()

# Print the intro
intro()

# Deal out the cards and start the game!
deal_cards()


# In[ ]:



