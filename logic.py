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

        self.current_card_suit = None
        self.current_card = None

        self.current_hidden_card_suit = None
        self.current_hidden_card = None

    def calc_multiplier(self):
        index = list(self.cards.keys()).index(self.current_card)
        above = len(self.cards) - index - 1
        below = index

        prob_higher = above / len(self.cards)
        prob_lower = below / len(self.cards)

        multiplier_higher = 1 / prob_higher if prob_higher != 0 else 1
        multiplier_lower = 1 / prob_lower if prob_lower != 0 else 1

        # 1.05 <= x <= 13
        multiplier_higher = max(1.05, min(multiplier_higher, 13))
        multiplier_lower = max(1.05, min(multiplier_lower, 13))

        rounded_higher = round(multiplier_higher / 0.05) * 0.05
        rounded_lower = round(multiplier_lower / 0.05) * 0.05

        return {
            "higher": round(rounded_higher, 2),
            "lower": round(rounded_lower, 2),
            "same": float(len(self.cards)),
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

    def get_card_resource_location(self, card, back=False):
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
        pass

    def get_current_card(self):
        pass

    def reset_game(self):
        pass


class Player:
    def __init__(self):
        self.balance = 500
        self.streak = 0
        self.bet = 0

    def validate_bet(self, amount):
        pass

    def place_bet(self, amount):
        pass

    def update_balance(self, multiplier):
        pass

    def get_balance(self):
        pass

    def increase_streak(self):
        pass

    def reset_streak(self):
        pass

    def get_streak(self):
        pass

    def check_if_bankrupt(self):
        pass


# For debugging
if __name__ == "__main__":
    higher_lower = HigherLower()
    card = higher_lower.draw_card()

    print(higher_lower.get_card_resource_location(card, True))
