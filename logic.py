import random


class HigherLower:
    def __init__(self):
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

    def calc_multiplier(self, card):
        index = list(self.cards.keys()).index(card)
        above = len(self.cards) - index - 1
        below = index

        prob_higher = above / len(self.cards)
        prob_lower = below / len(self.cards)

        multiplier_higher = 1 / prob_higher if prob_higher != 0 else 1
        multiplier_lower = 1 / prob_lower if prob_lower != 0 else 1

        rounded_higher = round(multiplier_higher / 0.05) * 0.05
        rounded_lower = round(multiplier_lower / 0.05) * 0.05

        return {
            "higher": round(rounded_higher, 2),
            "lower": round(rounded_lower, 2),
            "same": float(len(self.cards)),
        }

    def draw_card(self):
        pass

    def get_card_resource_location(self):
        pass

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
    print(higher_lower.calc_multiplier("5"))
