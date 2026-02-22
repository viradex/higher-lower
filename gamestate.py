class GameState:
    def __init__(self, player):
        self.player = player
        self.reset_all()

    def resolve_round(self, won, bet, multiplier, choice, player_card, dealer_card):
        self.balance = self.player.balance
        self.previous_balance = self.balance

        self.last_bet = bet
        self.last_multiplier = multiplier
        self.last_choice = choice
        self.won_last_round = won

        self.player_card = player_card
        self.dealer_card = dealer_card

        self.total_rounds += 1

        if won:
            self.streak += 1
            self.lose_streak = 0
        else:
            self.streak = 0
            self.lose_streak += 1

            self.lost_this_run = True

        if choice == "higher":
            self.high_streak += 1
            self.low_streak = 0
            self.same_streak = 0
        elif choice == "lower":
            self.low_streak += 1
            self.high_streak = 0
            self.same_streak = 0
        elif choice == "same":
            self.same_streak += 1
            self.high_streak = 0
            self.low_streak = 0

        self.lowest_balance_this_run = min(
            self.lowest_balance_this_run, self.player.balance
        )

        self.choice_history.append(choice)

        if won and multiplier >= 5:
            self.high_multiplier_streak += 1
        else:
            self.high_multiplier_streak = 0

        if not won and multiplier < 2:
            self.low_multiplier_loss_streak += 1
        else:
            self.low_multiplier_loss_streak = 0

        if won and multiplier < 1.2:
            self.low_multiplier_wins += 1

        if bet > 100:
            self.no_large_bets = False

    def reset_all(self):
        self.balance = self.player.balance
        # self.previous_balance = self.balance
        self.lowest_balance_this_run = self.balance

        self.streak = 0
        self.lose_streak = 0
        self.high_streak = 0
        self.low_streak = 0
        self.same_streak = 0
        self.choice_history = []

        self.high_multiplier_streak = 0
        self.low_multiplier_loss_streak = 0
        self.low_multiplier_wins = 0

        self.player_card = None
        self.dealer_card = None

        self.no_large_bets = True

        self.total_rounds = 0
        self.last_bet = 0
        self.last_multiplier = 1.0
        self.last_choice = None
        self.won_last_round = False
        self.lost_this_run = False
