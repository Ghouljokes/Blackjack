class Card:
    def __init__(self, value: int, name: str, suit: str) -> None:
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True

    def __repr__(self):
        return f"{self.suit}{self.name}"


deck: list[Card] = []
for suit_name in ["\u2665", "\u2666", "\u2660", "\u2663"]:
    deck.append(Card(11, "A", suit_name))
    for i in range(2, 11):
        deck.append(Card(i, str(i), suit_name))
    for face in ["J", "Q", "K"]:
        deck.append(Card(10, face, suit_name))
