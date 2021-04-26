from random import shuffle

ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
points = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


'''
Game Objects Here

'''

class Card:

#in order to create a Card we need a rank (Six) and a suit (Hearts)
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        # value of the card is not instantiated by a parameter, instead calculate it by global variables and our rank
        self.value = points[rank]

#string dunder/magic method in case we want to investigate the card using print()
    def __str__(self):
        return self.rank + " of " + self.suit
1

class Deck:

    def __init__(self):
        self.deck = []

        for _ in range(4):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(rank, suit))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.values = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def __str__(self):
        return (f"You have {self.cards}")

    def __repr__(self):
        return self.cards

    def add_card(self,card):
        self.cards.append(card)
        self.values += points[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        
        while self.values > 21 and self.aces:
            self.values -= 10
            self.aces -= 1


class Chips:
    
    def __init__(self, chips = 100):
        self.total = chips
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


'''
Game Functions Here

'''

def join_lines(strings):
    """
    Stack strings horizontally.
    This doesn't keep lines aligned unless the preceding lines have the same length.
    :param strings: Strings to stack
    :return: String consisting of the horizontally stacked input
    """
    liness = [string.splitlines() for string in strings]
    return '\n'.join(''.join(lines) for lines in zip(*liness))


def ascii_card(*cards):

    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :return: A string, the nice ascii version of cards
    """

    CARD = """\
 ┌─────────┐
 │{}       │
 │         │
 │    {}   │
 │         │
 │       {}│
 └─────────┘
    """.format('{rank: <2}', '{suit: <2}', '{rank: >2}')

    # we will use this to prints the appropriate icons for each card
    name_to_symbol = {
        'Spades':   '♠',
        'Diamonds': '♦',
        'Hearts':   '♥',
        'Clubs':    '♣',
    }

    def card_to_string(card):
        # 10 is the only card with a 2-char rank abbreviation
        rank = card.rank if card.rank == '10' else card.rank[0]

        # add the individual card on a line by line basis
        return CARD.format(rank=rank, suit=name_to_symbol[card.suit])


    return join_lines(map(card_to_string, cards))


def ascii_card_hidden(*cards):

    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """

    HIDDEN_CARD = """\
 ┌─────────┐
 │░░░░░░░░░│
 │░░░░░░░░░│
 │░░░░░░░░░│
 │░░░░░░░░░│
 │░░░░░░░░░│
 └─────────┘
    """
    return join_lines((HIDDEN_CARD,ascii_card(*cards[1:])))
 

def print_hidden():

    print(f'Current wallet ({player_chips.total}) - Current bet ({chips_on_table})')
    print(f'\nDealers hand ({dealer_hand.values-(dealer_hand.cards[0].value)}):')
    print(ascii_card_hidden(*dealer_hand.cards))
    print(f'Players hand ({player_hand.values}):')
    print(ascii_card(*player_hand.cards))

def print_show():

    print(f'\nDealers hand ({dealer_hand.values}):')
    print(ascii_card(*dealer_hand.cards))
    print(f'Players hand ({player_hand.values}):')
    print(ascii_card(*player_hand.cards))

def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:

        response = input("Hit or Stand? Enter 'h' or 's': ")
        print ("\n" * 100)
        if response[0].lower() == 'h':
            hit(deck,hand)
            print("\nPlayer Hits..")
            # print_hidden()
        
        elif response[0].lower() == 's':
            print("\nPlayer Stands..")
            playing = False
        
        else:
            print_hidden()
            print("\nPlease enter h or s only!\n")
            continue

        break

def player_busts(hand,dealer,chips):
    global playing

    print_show()
    print(f'YOU LOSE - Bust, your hand exceeds 21. You lost {chips_on_table} chips.')
    chips.lose_bet()
    playing = False
    pass

def player_wins(hand,dealer,chips):
    global playing
    print_show()
    print(f'YOU WIN - Your hand is higher. You gained {chips_on_table} chips.')
    chips.win_bet()
    playing = False
    pass

def dealer_busts(hand,dealer,chips):
    global playing
    print_show()
    print(f'YOU WIN - Dealer busts, hand is over 21. You gained {chips_on_table} chips.')
    chips.win_bet()
    playing = False
    pass

def dealer_wins(hand,dealer,chips):
    global playing
    print_show()
    print(f'YOU LOSE - Dealer has a higher hand. You lost {chips_on_table} chips.')
    chips.lose_bet()
    playing = False
    pass

def push(hand,dealer):
    global playing
    print_show()
    print('TIE - You both have the same value. You retain your bet.')
    playing = False
    pass

def take_bet(chips):
    while True:

        try:
            chips.bet = int(input("\nHow many chips would you like to bet?: "))
            print ("\n" * 100)
        except:
            print("\nSorry please provide an integer.")
        else:
            if chips.bet > chips.total:
                print(f'\nSorry, you dont have enough chips. {chips.total}')
            else:
                return chips.bet

def starting_chips():
    while True:
            value = input('\nEnter many chips would you like to start with: ')
            print ("\n" * 100)
            try:
                value = int(value)
                break
            except ValueError:
                print('\nERROR: Please enter a valid integer: ')
                continue
    return value

'''

Game Starts here

'''

print ("\n" * 100)
print("\n\n\nWELCOME TO BLACKJACK by Josh\n\n")
print("""\nBlackjack rules:

Dealer deals 2 cards to the players and two to himself (1 card face up, the other face down).

Blackjack card values: All cards count their face value in blackjack.
 Picture cards count as 10 and the ace can count as either 1 or 11.
 Card suits have no meaning in blackjack.
 he total of any hand is the sum of the card values in the hand

Players must decide whether to stand, hit, surrender, double down, or split.

The dealer acts last and must hit on 16 or less and stand on 17 through 21.

Players win when their hand totals higher than dealer’s hand, or they have 21 or less when the dealer busts.

Players lose their bet when they bust, or when their hand totals less than the dealer’s hand.

If the player’s and dealer’s hands total the same (known as a tie or push), the player retains his bet.\n""")

player_chips = Chips(starting_chips())
chips_on_table = take_bet(player_chips)

game_on = True

while game_on:

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())


    while playing:

        if player_hand.values < 21:
            print_hidden()
            hit_or_stand(deck,player_hand)

        if player_hand.values > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        
        
        while dealer_hand.values < 17:
            hit(deck,dealer_hand)
            print("\nDealer draws a card... ")
            if  playing:
                print_hidden()
                hit_or_stand(deck,player_hand)

        if dealer_hand.values > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.values > player_hand.values:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.values < player_hand.values:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        

    # Inform Player of their chips total 

    print(f'\nYour wallet is now at {player_chips.total} chips.')
    
    # Ask to play again
    new_game = input("\nWould you like to play another hand? Enter 'y': ")
    
    if new_game[0].lower()=='y':
        print ("\n" * 100)
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
