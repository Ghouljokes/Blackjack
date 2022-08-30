"""Hold deck of cards, as well as cards."""
from dataclasses import dataclass
import random


@dataclass
class Card:
    value: int  # How much card is worth
    name: str  # What card is called.


CARD_VALS = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

SUITS = ["\u2665", "\u2666", "\u2660", "\u2663"]  # suit symbols.


class Deck:
    """Deck of cards."""

    def __init__(self):
        """Create a full deck of cards."""
        self.cards: list[Card] = []
        self.fill_deck()

    def draw(self):
        """Draw a card from the deck."""
        card = self.cards.pop()
        return card

    def fill_deck(self):
        """Fill the deck with new set of cards."""
        self.cards = []  # Reset the deck.
        for suit in SUITS:
            for name, value in CARD_VALS.items():
                card_name = suit + name
                card = Card(value, card_name)
                self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        """Shuffle the cards randomly."""
        random.shuffle(self.cards)
