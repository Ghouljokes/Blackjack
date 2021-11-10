import random
import copy
import time

"""Stuff I wanna add:
    option for npc player(s)
    split
Stuff I need to do:
    organize the code relating to playing the game
"""
cards = []
id = 1
class Card:
    def __init__(self, value: int, name: str, suit: str) -> None:
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True
    
    def get_full_name(self) -> str:
        return f"{self.name} of {self.suit}"

for suit in ["hearts", "diamonds", "spades", "clubs"]:
    cards.append(Card(11, "Ace", suit))
    for i in range(2, 11):
        cards.append(Card(i, str(i), suit))
    for face in ["Jack", "Queen", "King"]:
        cards.append(Card(10, face, suit))


class Dude:
    def __init__(self, startingchips: int, name: str) -> None:
        self.hand = []
        self.total = 0
        self.chips = startingchips
        self.name = name
    
    def draw(self) -> None:
        to_draw = random.choice(cards)
        while not to_draw.in_deck:
            to_draw = random.choice(cards)
        to_draw.in_deck = False
        self.hand.append(copy.deepcopy(to_draw))
        if self.get_total() > 21:
            self.lower_ace()
    
    def debug_draw(self, index: int) -> None:
        self.hand.append(copy.deepcopy(cards[index]))

    def get_total(self) -> int:
        return sum([card.value for card in self.hand])

    def show_hand(self) -> str:
        return self.name + " hand: " + ", ".join(card.get_full_name() for card in self.hand)

    def lower_ace(self) -> None:
        for card in self.hand:
            if card.value == 11:
                card.value = 1
                return

    def auto_draw(self, goal: int, view_hand=True) -> None:
        while self.get_total() < goal:
            self.draw()
            if view_hand:
                print(self.show_hand())
                time.sleep(0.5)



def place_bet() -> int:
    bet = int(input("Place your bet: "))
    if bet > player.chips:
        print("You don't have enough chips!")
        return place_bet()
    if bet > dealer.chips:
        print("Dealer doesn't have that many chips!")
        return place_bet()
    return bet


def player_earns(amount: int) -> None:
    player.chips += amount
    dealer.chips -= amount


def play_round() -> None:
    print(f"House chips: {dealer.chips},  Player chips: {player.chips}")
    can_surrender = True
    your_bet = place_bet()
    can_double_down = your_bet * 2 <= player.chips
    for card in cards:
        card.in_deck = True
    dealer.hand = []
    player.hand = []
    dealer.draw()
    dealer.draw()
    player.draw()
    player.draw()
    print(f"Dealer's hand: {dealer.hand[0].get_full_name()}, hidden")

    if dealer.get_total() == 21:
        print(f"{dealer.show_hand()}\n Blackjack! Dealer wins {int(1.5 * your_bet)} chips.")
        player_earns(int(-1.5 * your_bet))
        return

    while player.get_total() < 21:
        print(player.show_hand())
        print("Your bet: " + str(your_bet))
        print("What would you like to do? Select a number:\n   1) hit\n   2) stay")
        if can_surrender:
            print("   3) surrender")
        if can_double_down:
            print("   4) double down")
        choice = input()
        if choice == "1":
            player.draw()
            can_surrender, can_double_down = False, False
        elif choice == "2":
            break
        elif choice == "3" and can_surrender:
            print(f"You surrender and lose {int(.5 * your_bet)} chips")
            player_earns(int(-.5 * your_bet))
            return
        elif choice == "4" and can_double_down:
            your_bet *= 2
            player.draw()
            break
        else:
            print("Please enter a valid choice.")
    print(player.show_hand())

    if player.get_total() == 21:
        print(f"Blackjack! You win {int(1.5 * your_bet)} chips.")
        player_earns(int(1.5 * your_bet))
        return
    elif player.get_total() > 21:
        print(f"You overshoot and lose {your_bet} chips.")
        player_earns(-your_bet)
        return

    time.sleep(0.5)
    print(dealer.show_hand())
    time.sleep(0.5)

    dealer.auto_draw(16)

    if dealer.get_total() > 21:
        print(f"House overshot. You gain {your_bet} chips")
        player_earns(your_bet) 
    elif dealer.get_total() > player.get_total():
        print(f"House wins. You lose {your_bet} chips")
        player_earns(-your_bet)
    elif dealer.get_total() < player.get_total():
        print(f"You win. You gain {your_bet} chips")
        player_earns(your_bet)
    else:
        print("Evened out")


player = Dude(1000, "Player")
dealer = Dude(5000, "Dealer")
while player.chips > 0 and dealer.chips > 0:
    play_round()
if player.chips <= 0:
    for i in range(100):
        print("You've gone and busted my good man. You've gone and busted my good man. You've gone and busted my good man. ")
elif dealer.chips <= 0:
    print("The dealers have had enough and banned you from the casino. Congratulations!")