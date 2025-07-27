class LongTermFocus:
    def __init__(self, core_goals):
        self.core_goals = core_goals
        self.active_focus = None

    def reinforce(self):
        print(" Long-term focus lock:", self.core_goals)
        self.active_focus = self.core_goals[0] if self.core_goals else "undefined"
