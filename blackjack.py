import random
import copy
import time
from dudesrock import Dude

"""Stuff I wanna add:
    option for npc player(s)
    split
Stuff I need to do:
    organize the code relating to playing the game
"""
deck = []
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
    deck.append(Card(11, "Ace", suit))
    for i in range(2, 11):
        deck.append(Card(i, str(i), suit))
    for face in ["Jack", "Queen", "King"]:
        deck.append(Card(10, face, suit))


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
    for card in deck:
        card.in_deck = True
    dealer.prep_round(deck)
    player.prep_round(deck)
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
            player.draw(deck)
            can_surrender, can_double_down = False, False
        elif choice == "2":
            break
        elif choice == "3" and can_surrender:
            print(f"You surrender and lose {int(.5 * your_bet)} chips")
            player_earns(int(-.5 * your_bet))
            return
        elif choice == "4" and can_double_down:
            your_bet *= 2
            player.draw(deck)
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

    dealer.auto_draw(16, deck)

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