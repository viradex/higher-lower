import random

# Formula for deciding higher/lower multiplier:
#
# M = S * (1 + N / 13)
#
# where M is multiplier, S is scaling factor (1.3),
# and N is number of cards above/below current card


class HigherLower:
    def __init__(self):
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.current_card = None
        self.scaling_factor = 1.3

    def calc_multiplier(self, card):
        pass

    def draw_card(self):
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
