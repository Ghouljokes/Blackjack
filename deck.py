class Card:
    def __init__(self, value: int, name: str, suit: str) -> None:
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True

    def __repr__(self):
        return f"{self.name} of {self.suit}"


deck: list[Card] = []
for suit_name in ["hearts", "diamonds", "spades", "clubs"]:
    deck.append(Card(11, "Ace", suit_name))
    for i in range(2, 11):
        deck.append(Card(i, str(i), suit_name))
    for face in ["Jack", "Queen", "King"]:
        deck.append(Card(10, face, suit_name))
