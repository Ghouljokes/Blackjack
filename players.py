from time import sleep
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main import Game
    from deck import Card


class BaseActor:
    """Base actor class"""

    game: "Game"

    def __init__(self, starting_chips: int, name: str):
        """Initialize the actor."""
        self.hand: list["Card"] = []
        self.chips = starting_chips
        self.name = name

    @property
    def chip_count(self):
        """What to display to show chips."""
        return f"{self.name} chips: {self.chips}"

    @property
    def deck(self):
        """Game deck."""
        return self.game.deck

    @property
    def total(self):
        """Get total value of hand."""
        return sum([card.value for card in self.hand])

    def draw(self):
        """Draw a card from a deck."""
        card = self.deck.draw()
        self.hand.append(card)
        if self.total > 21:
            self.lower_ace()  # Lower aces to keep total <= 21.

    def lower_ace(self):
        """Change value of first ace."""
        for card in self.hand:
            if card.value == 11:
                card.value = 1
                return

    def prep_round(self):
        """Set actor up for start of a round."""
        for _ in range(2):
            self.draw()

    def show_hand(self):
        """Show actor's full hand."""
        hand_str = ", ".join(card.name for card in self.hand)
        print(f"{self.name} hand: {hand_str}")
        print(f"{self.name} total: {self.total}")
        print()


class Player(BaseActor):
    """Player of the game."""

    def __init__(self, starting_chips: int, name: str):
        """Initialize the player."""
        super().__init__(starting_chips, name)
        self.bet = 0
        self.status = "unplayed"
        self.choices = {
            "1": self.hit,
            "2": self.stay,
            "3": self.surrender,
            "4": self.double_down,
        }

    @property
    def can_double_down(self):
        """Check if double down is allowed."""
        return self.has_not_drawn and self.bet * 2 <= self.dealer.chips

    @property
    def dealer(self):
        """Get game dealer."""
        return self.game.dealer

    @property
    def has_not_drawn(self):
        """Check if player has drawn yet."""
        return len(self.hand) == 2

    def draw(self):
        """Draw cards then set status."""
        super().draw()
        if self.total == 21:
            self.status = "blackjack"
        elif self.total > 21:
            self.status = "overshoot"

    def hit(self):
        """Hit and draw a card."""
        self.draw()
        print(f"{self.name} chooses to hit.")

    def stay(self):
        """Stay."""
        print(f"{self.name} chooses to stay.")
        self.status = "stay"

    def surrender(self):
        """Surrender half of the bet."""
        print(f"{self.name} chooses to surrender.")
        self.get_chips(-self.bet // 2)
        self.status = "surrender"
        self.bet = 0

    def double_down(self):
        """Double the bet and place one card."""
        print(f"{self.name} chooses to double down.")
        self.bet *= 2
        self.status = "doubledown"
        self.draw()

    def turn(self):
        """Make choices."""
        while self.status == "unplayed":
            if self == self.game.players[0]:
                self.show_hand()
            self.make_choice()

    def prep_round(self):
        """Same as BaseActor only set bet and status."""
        self.status = "unplayed"
        self.bet = 0
        for _ in range(2):
            self.draw()

    def get_chips(self, amount: int):
        """Give chips to player. A negative number takes chips."""
        self.chips += amount
        self.dealer.chips -= amount
        if amount > 0:
            print(f"Dealer gives {amount} chips to {self.name}")
        else:
            print(f"Dealer takes {-amount} chips from {self.name}")

    def make_choice(self):
        """Choose course of action. Overridden by subclasses."""
        raise NotImplementedError

    def place_bet(self):
        """Place a bet. Overridden by subclasses."""
        raise NotImplementedError


class HumanPlayer(Player):
    """User controlled player."""

    def __init__(self, starting_chips: int):
        """Set up player and get name."""
        name = input("What is your name?:\n")
        super().__init__(starting_chips, name)

    def place_bet(self):
        """Get bet from user."""
        bet = 0
        while True:
            bet_input = input("Please enter a bet: ")
            if not bet_input.isnumeric():
                print("Enter a number.")
                continue
            bet = int(bet_input)
            if bet <= 0:
                print("Enter a bet greater than zero.")
                continue
            if bet > self.chips:
                print("You don't have that much!")
                continue
            if bet > self.dealer.chips:
                print("Dealer doesn't have that much!")
                continue
            self.bet = bet
            return

    def make_choice(self):
        """Prompt player for choice."""
        valid_choices = ["1", "2"]
        print("Please select a number:\n   1) hit\n   2) stay")
        if self.has_not_drawn:
            print("   3) surrender")
            valid_choices.append("3")
        if self.can_double_down:
            print("   4) double down")
            valid_choices.append("4")
        choice = input()
        while choice not in valid_choices:
            choice = input("Please enter a valid choice.\n")
        action = self.choices[choice]
        action()  # perform action


class AiPlayer(Player):
    """Computer controlled player."""

    def place_bet(self):
        """Determine bet to match."""
        self.bet = self.chips // 3  # Initially bet third of chips.
        # Keep bet from exceeding available chips.
        self.bet = min(self.bet, self.dealer.chips)
        print(f"{self.name} bets {self.bet} chips.")

    def make_choice(self):
        """Determine move to make."""
        choice = "2"  # Default to stay
        if self.total in range(9, 12) and self.can_double_down:
            choice = "4"  # Double down
        if self.total < 16:
            choice = "1"  # Draw
        if self.total == 16 and self.has_not_drawn:
            choice = "3"  # Surrender
        action = self.choices[choice]
        action()


class Dealer(BaseActor):
    """Dealer in the game."""

    def __init__(self, starting_chips: int):
        """Set up dealer."""
        super().__init__(starting_chips, "Dealer")

    def dealer_draw(self):
        """Draw cards until 16 or overshoot."""
        while self.total < 16:
            sleep(0.5)
            self.draw()
            self.show_hand()
