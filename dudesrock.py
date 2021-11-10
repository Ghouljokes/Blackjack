import random
import copy
import time

class Dude:
    def __init__(self, startingchips: int, name: str) -> None:
        self.hand = []
        self.chips = startingchips
        self.name = name
        self.bet = 0
        self.can_surrender = True
        self.can_double_down = True
    
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
    
    def debug_draw(self, index: int, cards: list) -> None:
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

    def auto_draw(self, goal: int, cards: list, view_hand=True) -> None:
        while self.get_total() < goal:
            self.draw(cards)
            if view_hand:
                print(self.show_hand())
                #time.sleep(0.5)

    def earns_from(self, amount: int, earned_from: object) -> None:
        self.chips += amount
        earned_from.chips -= amount