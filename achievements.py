class Achievement:
    def __init__(self, key, name, description, hidden, condition):
        self.key = key
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

    def to_dict(self):
        pass

    def load_from_dict(self):
        pass


achievements = {}
