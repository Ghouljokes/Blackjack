import random
import copy


class Dude:
    def __init__(self, startingchips: int, name: str) -> None:
        self.hand = []
        self.chips = startingchips
        self.name = name
        self.bet = 0
        self.can_surrender = True
        self.can_double_down = True

    def place_bet(self, to_match: object) -> None:
        pass
    
    def draw(self, cards: list) -> None:
        to_draw = random.choice(cards)
        while not to_draw.in_deck:
            to_draw = random.choice(cards)
        to_draw.in_deck = False
        self.hand.append(copy.deepcopy(to_draw))
        if self.get_total() > 21:
            self.lower_ace()

    def prep_round(self, cards: list) -> None:
        self.hand = []
        self.draw(cards)
        self.draw(cards)
        self.can_surrender = True
        self.can_double_down = self.bet * 2 <= self.chips
    
    def get_total(self) -> int:
        return sum([card.value for card in self.hand])

    def show_hand(self) -> None:
        print(f"{self.name} hand: {', '.join(card.__repr__() for card in self.hand)}")
        print(f"{self.name} total: {self.get_total()}")

    def lower_ace(self) -> None:
        for card in self.hand:
            if card.value == 11:
                card.value = 1
                return

    def earns_from(self, amount: int, earned_from: object) -> None:
        self.chips += amount
        earned_from.chips -= amount


class Airobot(Dude):
 
    def place_bet(self, to_match: Dude) -> None:
        self.bet = self.chips // 3
        if self.bet > to_match.chips:
            self.bet = to_match.chips
        elif self.bet <= 10:
            self.bet = self.chips
        print(f"{self.name} bets {self.bet} chips.")

    def make_choice(self) -> str:
        if self.get_total() in range(9, 12) and self.can_double_down:
            return "4"
        elif self.get_total() < 16:
            return "1"
        elif self.get_total() == 16 and self.can_surrender:
            return "3"
        else:
            return "2"


class User(Dude):

    def place_bet(self, to_match: Dude) -> None:
        self.bet = input("Place your bet: ")
        if self.bet.isnumeric():
            self.bet = int(self.bet)
        else:
            print("Please enter a number.")
            self.place_bet(to_match)
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
