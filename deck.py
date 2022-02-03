class Card:
    def __init__(self, value: int, name: str, suit: str) -> None:
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True

    def __repr__(self):
        return f"{self.suit}{self.name}"


card_vals = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
             "K": 10}
deck: list[Card] = []
for suit_name in ["\u2665", "\u2666", "\u2660", "\u2663"]:
    for name, val in card_vals.items():
        deck.append(Card(val, name, suit_name))
