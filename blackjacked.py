from dudesrock import Dude, User, Airobot
from deck import deck

dealer = Dude(5000, "Dealer")

print("Enter your preferred mode of play:")
print("    1) User controlled")
print("    2) Automatic")
BOT_OR_NOT = "3"
while True:
    bot_or_not = input()
    if bot_or_not in ["1", "2"]:
        break
    print("Please enter a valid number.")


player1 = User(1000, input("What is your name?\n")) if bot_or_not == "1" else Airobot(1000, "BJbot")


def play_round(player: Dude) -> None:
    """Simulate a round of blackjack"""
    print("NEW ROUND")
    print(f"House chips: {dealer.chips}, {player} chips: {player.chips}")
    for card in deck:
        card.in_deck = True
    player.place_bet(dealer)
    dealer.prep_round(deck)
    player.prep_round(deck)
    print(f"Dealer's hand: {dealer.hand[0]}, hidden")

    if dealer.get_total() == 21:
        dealer.show_hand()
        print(f"Blackjack! Dealer wins {int(1.5 * player.bet)} chips.")
        player.earns_from(int(-1.5 * player.bet), dealer)
        return

    while player.get_total() < 21:
        player.show_hand()
        choice = player.make_choice()
        if choice == "1":
            player.draw(deck)
            print(f"{player} chooses to hit.")
            player.can_surrender, player.can_double_down = False, False
        elif choice == "2":
            print(f"{player} chooses to stay.")
            break
        elif choice == "3":
            print(f"{player} surrenders, giving up {player.bet//2} chips.")
            player.earns_from(int(-.5 * player.bet), dealer)
            return
        else:
            print(f"{player} chooses to double down.")
            player.bet *= 2
            player.draw(deck)
            break

    player.show_hand()

    if player.get_total() == 21:
        print(f"Blackjack! {player} wins {int(1.5 * player.bet)} chips.")
        player.earns_from(int(1.5 * player.bet), dealer)
        return
    if player.get_total() > 21:
        print(f"{player} overshoots and loses {player.bet} chips.")
        player.earns_from(-player.bet, dealer)
        return

    dealer.show_hand()

    while dealer.get_total() < 16:
        dealer.draw(deck)
        dealer.show_hand()

    if dealer.get_total() > 21:
        print(f"House overshot. {player} gains {player.bet} chips.")
        player.earns_from(player.bet, dealer)
    elif dealer.get_total() > player.get_total():
        print(f"House wins. {player} loses {player.bet} chips.")
        player.earns_from(-player.bet, dealer)
    elif dealer.get_total() < player.get_total():
        print(f"{player} wins. {player} gains {player.bet} chips.")
        player.earns_from(player.bet, dealer)
    else:
        print("Evened out")


while player1.chips > 0 and dealer.chips > 0:
    play_round(player1)
if player1.chips <= 0:
    print(f"{player1} lost all their chips.")
elif dealer.chips <= 0:
    print("The casino is now bankrupt.")
