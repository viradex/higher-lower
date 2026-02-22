class AchievementManager:
    def __init__(self, achievements):
        self.achievements = achievements
        self.save_data_file = "hl-achievements.json"

    def check_achievements(self, game_state):
        pass

    def unlock(self, achievement):
        pass

    def get_unlocked(self):
        pass

    def get_locked(self):
        pass

    def update_data(self):
        pass

    def get_data(self):
        pass

    def create_file(self):
        pass

    def reset(self):
        pass


class Achievement:
    def __init__(self, name, description, hidden, condition):
        self.name = name
        self.description = description
        self.hidden = hidden
        self.condition = condition
        self.unlocked = False

    @property
    def display_name(self):
        if self.hidden and not self.unlocked:
            return "???"
        return self.name

    @property
    def display_description(self):
        if self.hidden and not self.unlocked:
            return "Keep playing to discover this achievement!"
        return self.description

    def check(self, game_state):
        if not self.unlocked and self.condition(game_state):
            self.unlocked = True
            return True
        return False


achievements = {
    # === Streaks === #
    "streak_3": Achievement(
        "Lucky Guess",
        "Guess correctly three times in a row.",
        False,
        lambda gs: gs.streak >= 3,
    ),
    "streak_5": Achievement(
        "On Fire",
        "Guess correctly five times in a row.",
        False,
        lambda gs: gs.streak >= 5,
    ),
    "streak_10": Achievement(
        "Unstoppable",
        "Guess correctly ten times in a row.",
        False,
        lambda gs: gs.streak >= 10,
    ),
    "streak_15": Achievement(
        "Card Psychic",
        "Guess correctly fifteen times in a row.",
        False,
        lambda gs: gs.streak >= 15,
    ),
    "streak_20": Achievement(
        "Built Different",
        "Guess correctly twenty times in a row.",
        False,
        lambda gs: gs.streak >= 20,
    ),
    # === Balance === #
    "balance_1k": Achievement(
        "Double-Down",
        "Reach $1000 in balance.",
        False,
        lambda gs: gs.balance >= 1000,
    ),
    "balance_2k": Achievement(
        "High Roller",
        "Reach $2000 in balance.",
        False,
        lambda gs: gs.balance >= 2000,
    ),
    "balance_5k": Achievement(
        "Casino King",
        "Reach $5000 in balance.",
        False,
        lambda gs: gs.balance >= 5000,
    ),
    "balance_10k": Achievement(
        "Let's Go Gambling!",
        "Reach $10,000 in balance.",
        False,
        lambda gs: gs.balance >= 10000,
    ),
    "balance_100k": Achievement(
        "Kind of a Millionaire",
        "Reach $100,000 in balance.",
        False,
        lambda gs: gs.balance >= 100000,
    ),
    # === Risk and Luck ===  #
    "win_bet_all": Achievement(
        "Going All In",
        "Bet your entire balance (more than $5000) and win!",
        False,
        lambda gs: gs.won_last_round
        and gs.previous_balance >= 5000
        and gs.last_bet == gs.previous_balance,
    ),
    "win_with_min_balance": Achievement(
        "Clutching Up",
        "Win a bet with only $50 in balance remaining.",
        True,
        lambda gs: gs.won_last_round and gs.previous_balance == 50,
    ),
    "win_x10_multiplier": Achievement(
        "Risk Taker",
        "Win a bet with a multiplier of x10 or more.",
        False,
        lambda gs: gs.won_last_round and gs.last_multiplier >= 10.0,
    ),
    "win_same_bet": Achievement(
        "Same Old, Same Old",
        "Win a 'same' bet.",
        True,
        lambda gs: gs.won_last_round and gs.last_choice == "same",
    ),
    "lose_low_multiplier": Achievement(
        "That Should've Worked",
        "Lose a bet after betting on a x1.05 multiplier.",
        True,
        lambda gs: not gs.won_last_round and gs.last_multiplier <= 1.05,
    ),
    "lose_all_balance": Achievement(
        "All Gone Wrong",
        "Lose your entire balance (more than $5000) and go bankrupt.",
        True,
        lambda gs: not gs.won_last_round
        and gs.previous_balance >= 5000
        and gs.balance == 0,
    ),
    "high_multiplier_streak": Achievement(
        "Mathematically Improbable",
        "Win three x5 multipliers or more in a row.",
        True,
        lambda gs: gs.high_multiplier_streak >= 3,
    ),
    "higher_streak": Achievement(
        "Faithful to the High",
        "Pick 'higher' five times in a row.",
        True,
        lambda gs: gs.high_streak >= 5,
    ),
    "lower_streak": Achievement(
        "Faithful to the Low",
        "Pick 'lower' five times in a row.",
        True,
        lambda gs: gs.low_streak >= 5,
    ),
    "same_streak": Achievement(
        "Middle Enjoyer",
        "Pick 'same' five times in a row.",
        True,
        lambda gs: gs.same_streak >= 5,
    ),
    "streak_lose_5": Achievement(
        "Down Bad",
        "Lose five times in a row.",
        True,
        lambda gs: gs.lose_streak >= 5,
    ),
    "alternate_choice": Achievement(
        "Indecisive",
        "Alternate between 'high' and 'low' ten times.",
        False,
        lambda gs: (
            len(gs.choice_history) >= 10
            and all(
                gs.choice_history[-i] != gs.choice_history[-i - 1]
                and gs.choice_history[-i] in ("higher", "lower")
                and gs.choice_history[-i - 1] in ("higher", "lower")
                for i in range(1, 10)
            )
        ),
    ),
    "no_large_bets_win": Achievement(
        "Slow and Steady",
        "Reach $2000 without betting over $100.",
        False,
        lambda gs: gs.balance >= 2000 and gs.no_large_bets,
    ),
    "low_multiplier_wins": Achievement(
        "Penny Pincher",
        "Win ten bets where the multiplier is below x1.2.",
        True,
        lambda gs: gs.low_multiplier_wins >= 10,
    ),
    "low_multiplier_loss_streak": Achievement(
        "The House Always Wins",
        "Lose three times in a row when betting on a multiplier less than x2.",
        True,
        lambda gs: gs.low_multiplier_loss_streak >= 3,
    ),
    "low_to_high_balance": Achievement(
        "Ultimate Comeback",
        "Get your balance from $50 to $1000.",
        True,
        lambda gs: gs.lowest_balance_this_run <= 50 and gs.balance >= 1000,
    ),
    "middle_correct_guess": Achievement(
        "Lucky Seven",
        "Guess correctly when getting a card value of 7.",
        False,
        lambda gs: gs.won_last_round and gs.player_card == "7",
    ),
    "middle_same_guess": Achievement(
        "Not Like the Others",
        "Guess 'same' when getting a card value of 7 and win.",
        True,
        lambda gs: gs.won_last_round
        and gs.player_card == "7"
        and gs.last_choice == "same",
    ),
    "win_first_3": Achievement(
        "Hot Start",
        "Win the first three rounds of a run.",
        True,
        lambda gs: gs.total_rounds <= 3 and gs.streak >= 3,
    ),
    "reach_5k_no_loss": Achievement(
        "Untouchable",
        "Reach $5000 without losing a single round.",
        False,
        lambda gs: gs.balance >= 5000 and not gs.lost_this_run,
    ),
    "funny_number": Achievement(
        "SIIIXXX SEVEEEEEENNNNN!!!!",
        "Get your card to have a value of 6 and the dealer's card to have a value of 7.",
        True,
        lambda gs: gs.won_last_round
        and gs.player_card == "6"
        and gs.dealer_card == "7",
    ),
}
