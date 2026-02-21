import random
from pathlib import Path
import os


class HigherLower:
    def __init__(self):
        self.card_suits = [
            "AS",
            "2S",
            "3S",
            "4S",
            "5S",
            "6S",
            "7S",
            "8S",
            "9S",
            "10S",
            "JS",
            "QS",
            "KS",
            "AH",
            "2H",
            "3H",
            "4H",
            "5H",
            "6H",
            "7H",
            "8H",
            "9H",
            "10H",
            "JH",
            "QH",
            "KH",
            "AD",
            "2D",
            "3D",
            "4D",
            "5D",
            "6D",
            "7D",
            "8D",
            "9D",
            "10D",
            "JD",
            "QD",
            "KD",
            "AC",
            "2C",
            "3C",
            "4C",
            "5C",
            "6C",
            "7C",
            "8C",
            "9C",
            "10C",
            "JC",
            "QC",
            "KC",
        ]

        self.cards = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
        }

        self.current_card = None
        self.current_card_suit = None

        self.current_hidden_card = None
        self.current_hidden_card_suit = None

        self.house_edge = 0.05  # 5%

    def calc_multiplier(self):
        """
        Calculate the multiplier for higher, lower, and same value bets,
        based on the card in `self.current_card`.

        ---

        Let:
        - `M` be the multiplier
        - `h` be the house edge
        - `W` be the number of possible winning cards

        The multiplier for 'higher' and 'lower' is calculated using the formula: `M = (51 ∙ (1 - h)) / W` where `W ≠ 0`.
        If `W` is 0, the multiplier is 0.

        The 'same' multiplier has a constant value of 16.

        The multiplier is limited to the range `M ∈ [1.05, 16]`.
        """
        if self.current_card is None:
            raise ValueError("No current card drawn.")

        cards = list(self.cards.keys())
        index = cards.index(self.current_card)

        above = len(cards) - index - 1
        below = index

        total_remaining = 51

        higher_cards = above * 4
        lower_cards = below * 4

        def fair_multiplier(winning_cards):
            if winning_cards == 0:
                return 0
            prob = winning_cards / total_remaining

            value = 1 / prob
            value *= 1 - self.house_edge

            value = max(round(value / 0.05) * 0.05, 1.05)
            return round(value, 2)

        return {
            "higher": fair_multiplier(higher_cards),
            "lower": fair_multiplier(lower_cards),
            "same": 17,
        }

    def draw_card(self):
        card = random.choice(self.card_suits)

        self.current_card_suit = card
        self.current_card = card[:-1]
        return card

    def draw_hidden_card(self):
        if self.current_card is None:
            raise TypeError("Call draw_card() before draw_hidden_card()")

        valid_cards = [
            card for card in self.card_suits if card != self.current_card_suit
        ]
        card = random.choice(valid_cards)

        self.current_hidden_card_suit = card
        self.current_hidden_card = card[:-1]
        return card

    def get_card_img_path(self, card, back=False):
        if back:
            path = f"assets/back/{random.randint(1, 6)}.png"
        else:
            path = f"assets/{card[:-1]}/{card}.png"

        if not Path(path).exists():
            raise FileNotFoundError(
                f"Could not find image file {path} from current directory {os.getcwd()}"
            )

        return path

    def make_guess(self, guess):
        valid_guesses = ("higher", "lower", "same")
        guess = guess.lower()

        if guess not in valid_guesses:
            raise ValueError(f"Invalid guess, received {guess}")
        elif self.current_card is None or self.current_hidden_card is None:
            raise TypeError(
                "Call draw_card() and draw_hidden_card() before making a guess"
            )

        cards = list(self.cards.keys())
        reference_index = cards.index(self.current_card)
        value_index = cards.index(self.current_hidden_card)

        if value_index < reference_index:
            answer = "lower"
        elif value_index > reference_index:
            answer = "higher"
        else:
            answer = "same"

        return guess == answer

    def reset_game(self):
        self.current_card = None
        self.current_card_suit = None
        self.current_hidden_card = None
        self.current_hidden_card_suit = None


class Player:
    def __init__(self):
        self.balance = 500
        self.streak = 0
        self.bet = 0
        self.currently_betting = False
        self.min_bet = 50

    def validate_bet(self, amount):
        if amount < self.min_bet or amount > self.balance:
            return False

        return True

    def place_bet(self, amount):
        self.bet = amount
        self.balance -= amount
        self.currently_betting = True

        return self.balance

    def done_bet(self):
        self.currently_betting = False

    def update_balance(self, multiplier):
        amount = round(self.bet * multiplier)

        self.balance += amount
        return amount

    def increase_balance(self, amount):
        self.balance += amount
        return self.balance

    def increase_streak(self):
        self.streak += 1
        return self.streak

    def reset_streak(self):
        self.streak = 0
        return self.streak

    def is_bankrupt(self):
        if self.balance < self.min_bet:
            return True

        return False

    def reset_bet(self):
        self.bet = 0
        self.currently_betting = False

    def reset_game(self):
        self.balance = 500
        self.streak = 0
        self.bet = 0
        self.currently_betting = False


# For debugging
if __name__ == "__main__":
    higher_lower = HigherLower()
    player = Player()
