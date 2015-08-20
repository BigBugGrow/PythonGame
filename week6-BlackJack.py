import simplegui
import random

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

in_play = False
outcome = ""
cash = 100
bet_made = False
bet = 0

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        message = "Hand contains "
        for card in self.hand:
            message = message + str(card) + " "
        return message

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        self.value = 0
        for card in self.hand:
            card = str(card)
            self.value += VALUES[card[1]]
        for card in self.hand:
            card = str(card)
            if card[1] == "A":
                if self.value < 12:
                    self.value += 10
        return self.value
   
    def draw(self, canvas, x, y):
        position = [x, y]
        hand_len = len(self.hand)
        while hand_len > 0:
            for card in self.hand:
                card.draw(canvas, position)
                hand_len -= 1
                position[0] += 100
        
class Deck:
    def __init__(self):
        self.deck = []
        for rank in RANKS:
            for suit in SUITS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        message = "Deck contains "
        for card in self.deck:
            message = message + str(card) + " "
        return message

def deal():
    global game_deck, hand_player, hand_dealer, in_play, outcome, bet_made, cash, bet, outcome
    if cash != 0:
        if bet_made is True:
            cash -= bet
            bet = 0
            bet_made = False
        game_deck = Deck()
        game_deck.shuffle()
        hand_player = Hand()
        hand_dealer = Hand()
        for time in range(2):
            drawn_card = game_deck.deal_card()
            hand_player.add_card(drawn_card)
        for time in range(2):
            drawn_card = game_deck.deal_card()
            hand_dealer.add_card(drawn_card)
        outcome = "Make bet"
        if cash == 0:
                outcome = "Gone broke. Reset?"
        else:
            in_play = True

def hit():
    global game_deck, hand_player, in_play, outcome, cash, bet, bet_made
    if in_play is True:
        if bet_made is True:
            drawn_card = game_deck.deal_card()
            hand_player.add_card(drawn_card)
            score = hand_player.get_value()
            if score > 21:
                outcome = "You busted. Deal?"
                cash -= bet
                bet = 0
                bet_made = False
                in_play = False
                if cash == 0:
                    outcome = "Gone broke. Reset?"
        else:
            outcome = "Make bet"
        
       
def stand():
    global game_deck, hand_player, cash, bet_made, bet, hand_dealer, in_play, outcome
    if in_play is True:
        if bet_made is True:
            while hand_dealer.get_value() < 17:
                drawn_card = game_deck.deal_card()
                hand_dealer.add_card(drawn_card)
            if hand_dealer.get_value() > 21:
                outcome = "You win! Deal?"
                cash += bet
                bet = 0
                bet_made = False
                in_play = False
            else:
                player_score = hand_player.get_value()
                dealer_score = hand_dealer.get_value()
                if player_score > dealer_score:
                    outcome = "You win! Deal?"
                    cash += bet
                    bet = 0
                    bet_made = False
                    in_play = False
                else:
                    outcome = "Dealer wins! Deal?"
                    cash -= bet
                    bet = 0
                    bet_made = False
                    if cash == 0:
                        outcome = "Gone broke. Reset?"
                    in_play = False
        else:
            outcome = "Make bet"
    else:
        pass
    
def draw(canvas):
    global card_back, in_play, bet, cash
    canvas.draw_text('BLACKJACK', (20, 80), 70, 'Black', 'monospace')
    canvas.draw_text('Your hand:', (30, 135), 20, 'Black', 'monospace')
    canvas.draw_text('Dealer hand:', (30, 290), 20, 'Black', 'monospace')
    hand_player.draw(canvas, 30, 150)
    hand_dealer.draw(canvas, 30, 305)
    if in_play is True:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, (65, 353), CARD_SIZE)
    canvas.draw_text(outcome, (30, 490), 50, 'black', 'monospace')
    canvas.draw_text("Round bet: " + str(bet), (35, 550), 20, 'black', 'monospace')
    canvas.draw_text("Total cash: " + str(cash), (35, 575), 20, 'black', 'monospace')

def input_handler(text_input):
    global bet, bet_made, cash, outcome
    try:
        if bet_made is False and in_play is True:
            if 0 <= int(text_input) <= cash:
                bet = int(text_input)
                outcome = "Hit or stand?"
                bet_made = True
    except:
        ValueError
        
def reset():
    global in_play, bet, cash, bet_made
    bet_made = in_play = False
    bet = 0
    cash = 100
    deal()
    
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset", reset, 200)
frame.set_draw_handler(draw)
inp = frame.add_input('Bet?', input_handler, 50)

deal()
frame.start()