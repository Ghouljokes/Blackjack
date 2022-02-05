"""random module."""
import random
# copy module.
import copy
from unicodedata import name


class Card:
    """represents a playing card."""

    def __init__(self, value: int, name: str, suit: str) -> None:
        """Initialize card."""
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True

    def __repr__(self):
        """Represent card as suit and name."""
        return f"{self.suit}{self.name}"


card_vals = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
             "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
             "J": 10, "Q": 10, "K": 10}

deck: list[Card] = []
for suit_name in ["\u2665", "\u2666", "\u2660", "\u2663"]:
    for card_name, val in card_vals.items():
        deck.append(Card(val, card_name, suit_name))


class Dude:
    """represents a player or dealer."""

    def __init__(self, startingchips: int, name: str, sentient: bool) -> None:
        """Initialize dude."""
        self.hand: list[Card] = []
        self.chips = startingchips
        self.name = name
        self.aware = sentient
        self.bet = 0
        self.can_surrender = True
        self.can_double_down = True

    def __repr__(self) -> str:
        """Represent dude as its name."""
        return self.name

    def place_bet(self, to_match) -> None:
        """Place a bet."""
        if self.aware:
            while True:
                bet = input("Place your bet: ")
                if bet.isnumeric():
                    self.bet = int(bet)
                    break
                print("Please enter a number.")
            if self.bet > self.chips:
                print("You don't have enough chips!")
                self.place_bet(to_match)
            if self.bet > to_match.chips:
                print(f"{to_match.name} doesn't have that many chips!")
                self.place_bet(to_match)
        else:
            self.bet = self.chips // 3
            if self.bet > to_match.chips:
                self.bet = to_match.chips
            elif self.bet <= 10:
                self.bet = self.chips
            print(f"{self.name} bets {self.bet} chips.")

    def make_choice(self) -> str:
        """Choose course of action."""
        if self.aware:
            valid_choices = ["1", "2"]
            print("Please select a number:\n   1) hit\n   2) stay")
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
        if self.get_total() in range(9, 12) and self.can_double_down:
            return "4"
        if self.get_total() < 16:
            return "1"
        if self.get_total() == 16 and self.can_surrender:
            return "3"
        return "2"

    def draw(self, cards: list) -> None:
        """Draw a card from a deck."""
        to_draw = random.choice(cards)
        while not to_draw.in_deck:
            to_draw = random.choice(cards)
        to_draw.in_deck = False
        self.hand.append(copy.deepcopy(to_draw))
        if self.get_total() > 21:
            self.lower_ace()

    def prep_round(self, cards: list) -> None:
        """Readies player for start of round."""
        self.hand = []
        self.draw(cards)
        self.draw(cards)
        self.can_surrender = True
        self.can_double_down = self.bet * 2 <= self.chips

    def get_total(self) -> int:
        """Get total value of hand."""
        return sum([card.value for card in self.hand])

    def show_hand(self) -> None:
        """Show each card in dude's hand."""
        hand_str = ', '.join(card.__repr__() for card in self.hand)
        print(f"{self.name} hand: {hand_str}")
        print(f"{self.name} total: {self.get_total()}")
        print()

    def lower_ace(self) -> None:
        """Change value of first available ace from 11 to 1."""
        for card in self.hand:
            if card.value == 11:
                card.value = 1
                return

    def earns_from(self, amount: int, earned_from) -> None:
        """Get chips from other dude."""
        self.chips += amount
        earned_from.chips -= amount
