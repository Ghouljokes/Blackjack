import time
from dudesrock import Dude
from deck import deck as deck

#MAKE IT SO YOU CAN CHOOSE YOUR OWN NAME FOR THE PLAYER

class User(Dude):

    def place_bet(self, to_match: object) -> None:
        self.bet = int(input("Place your bet: "))
        if self.bet > self.chips:
            print("You don't have enough chips!")
            self.place_bet(to_match)
        if self.bet > to_match.chips:
            print(f"{to_match.name} doesn't have that many chips!")
            self.place_bet(to_match)

    def make_choice(self) -> str:
        valid_choices = ["1", "2"]
        print("What would you like to do? Select a number:\n   1) hit\n   2) stay")
        if self.can_surrender:
            print("   3) surrender")
            valid_choices.append("3")
        if self.can_double_down:
            print("   4) double down")
            valid_choices.append("4")
        choice = input()
        while choice not in valid_choices:
            choice = input("Please enter a valid choice.\n")
        return choice


dealer = Dude(5000, "Dealer")
player1 = User(1000, input("What is your name?\n"))


def play_round(player: object) -> None:
    print("NEW ROUND")
    print(f"House chips: {dealer.chips}, {player.name}'s chips: {player.chips}")
    player.place_bet(dealer)
    for card in deck:
        card.in_deck = True
    dealer.prep_round(deck)
    player.prep_round(deck)
    print(f"Dealer's hand: {dealer.hand[0].get_full_name()}, hidden")

    if dealer.get_total() == 21:
        print(f"{dealer.show_hand()}\n Blackjack! Dealer wins {int(1.5 * player.bet)} chips.")
        player.earns_from(int(-1.5 * player.bet), dealer)
        return

    while player.get_total() < 21:
        print(player.show_hand())
        choice = player.make_choice()
        if choice == "1":
            player.draw(deck)
            print(f"{player.name} chooses to hit.")
            player.can_surrender, player.can_double_down = False, False
        elif choice == "2":
            print(f"{player.name} chooses to stay.")
            break
        elif choice == "3":
            print(f"{player.name} surrenders and gives up {int(.5 * player.bet)} chips.")
            player.earns_from(int(-.5 * player.bet), dealer)
            return
        else:
            print(f"{player.name} chooses to double down.")
            player.bet *= 2
            player.draw(deck)
            break

    print(player.show_hand())

    if player.get_total() == 21:
        print(f"Blackjack! {player.name} wins {int(1.5 * player.bet)} chips.")
        player.earns_from(int(1.5 * player.bet), dealer)
        return
    if player.get_total() > 21:
        print(f"{player.name} overshoots and loses {player.bet} chips.")
        player.earns_from(-player.bet, dealer)
        return

    print(dealer.show_hand())

    dealer.auto_draw(16, deck)

    if dealer.get_total() > 21:
        print(f"House overshot. {player.name} gains {player.bet} chips.")
        player.earns_from(player.bet, dealer) 
    elif dealer.get_total() > player.get_total():
        print(f"House wins. {player.name} loses {player.bet} chips.")
        player.earns_from(-player.bet, dealer)
    elif dealer.get_total() < player.get_total():
        print(f"{player.name} wins. {player.name} gains {player.bet} chips.")
        player.earns_from(player.bet, dealer)
    else:
        print("Evened out")


while player1.chips > 0 and dealer.chips > 0:
    play_round(player1)
if player1.chips <= 0:
    for i in range(100):
        print("You've gone and busted my good man. You've gone and busted my good man. You've gone and busted my good man. ")
elif dealer.chips <= 0:
    print("The dealers have had enough and banned you from the casino. Congratulations!")