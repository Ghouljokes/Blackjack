class Card:
    def __init__(self, value: int, name: str, suit: str) -> None:
        self.value = value
        self.name = name
        self.suit = suit
        self.in_deck = True
    
    def get_full_name(self) -> str:
        return f"{self.name} of {self.suit}"


deck: list[Card] = []
for suit in ["hearts", "diamonds", "spades", "clubs"]:
    deck.append(Card(11, "Ace", suit))
    for i in range(2, 11):
        deck.append(Card(i, str(i), suit))
    for face in ["Jack", "Queen", "King"]:
        deck.append(Card(10, face, suit))
