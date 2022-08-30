"""Hold the main game."""
from re import A
from deck import Deck
from players import HumanPlayer, AiPlayer, BaseActor, Player, Dealer

DEALER_STARTING_CHIPS = 20000
PLAYER_STARTING_CHIPS = 200


class Game:
    """Main game."""

    def __init__(self):
        """Set up game elements."""
        BaseActor.game = self
        self.deck = Deck()
        self.dealer = Dealer(DEALER_STARTING_CHIPS)
        self.players: list[Player] = []

    @property
    def in_players(self):
        """All players who've stayed or doubled down."""
        return [
            player for player in self.players if player.status in ["stay", "doubledown"]
        ]

    def reset_deck(self):
        """Return all cards to the deck."""
        self.deck.fill_deck()
        self.dealer.hand = []
        for player in self.players:
            player.hand = []

    def get_players(self):
        """Create players."""
        print("Enter your preferred mode of play:")
        print("    1) User controlled")
        print("    2) Automatic")
        while True:
            include_player = input()
            if include_player in ["1", "2"]:
                break
            print("Please choose 1 or 2.")
        if include_player == "1":
            player_one = HumanPlayer(PLAYER_STARTING_CHIPS)
        else:
            player_one = AiPlayer(PLAYER_STARTING_CHIPS, "BJBot")
        self.players.append(player_one)
        opponent_amount = 0
        print("How many ai opponents do you want? (Up to 3)")
        while True:
            amount_choice = input()
            if amount_choice in ["0", "1", "2", "3"]:
                break
            print("Please enter a valid number.")
        opponent_amount = int(amount_choice)
        for i in range(opponent_amount):
            name = "p" + str(i + 1)
            opponent = AiPlayer(PLAYER_STARTING_CHIPS, name)
            self.players.append(opponent)

    def prep_round(self):
        """Set up a new round."""
        print("\n\nNEW ROUND\n\n")
        print(self.dealer.chip_count)
        print(", ".join([player.chip_count for player in self.players]))
        self.reset_deck()
        self.dealer.prep_round()
        for player in self.players:
            player.prep_round()
            player.place_bet()

    def play_round(self):
        """Simulate a round of blackjack."""
        self.prep_round()
        print(f"Dealer's hand: {self.dealer.hand[0].name}, hidden")

        if self.dealer.total == 21:
            self.dealer.show_hand()
            print(f"Blackjack! Dealer gets everyone's bets.")
            for player in self.players:
                player.get_chips(-player.bet)
            return

        for player in self.players:
            player.turn()
        # post_draws loop.
        for player in self.players:
            player.show_hand()
            if player.status == "blackjack":
                winnings = int(1.5 * player.bet)
                print(f"Blackjack! {player.name} wins {winnings} chips.")
                player.get_chips(winnings)
            elif player.status == "overshoot":
                print(f"{player.name} overshoots.")
                player.get_chips(-player.bet)

        self.dealer.show_hand()
        in_players = self.in_players
        if in_players:  # If there are hands to match
            self.dealer.dealer_draw()
            if self.dealer.total > 21:
                print(f"Dealer Overshot.")
                for player in in_players:
                    player.get_chips(player.bet)
            else:
                for player in in_players:
                    if self.dealer.total > player.total:
                        player.get_chips(-player.bet)
                    elif self.dealer.total < player.total:
                        player.get_chips(player.bet)
                    else:
                        print(f"{player.name} evened out.")

    def play_game(self):
        self.get_players()
        while self.dealer.chips > 0 and len(self.players) > 0:
            self.play_round()
            for player in self.players:
                if player.chips <= 0:
                    print(f"{player.name} is out!")
                    self.players.remove(player)
        if len(self.players) == 0:
            print("Hey kid... The house always wins.")
        elif self.dealer.chips <= 0:
            winner = max(self.players, key=lambda player: player.chips)
            print(f"{winner.name} wins!")


if __name__ == "__main__":
    new_game = Game()
    new_game.play_game()
