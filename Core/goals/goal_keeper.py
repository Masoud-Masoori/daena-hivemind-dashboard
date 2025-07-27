class GoalKeeper:
    def __init__(self, core_goal=""):
        self.core_goal = core_goal

    def reinforce(self):
        print(f" Remember your mission: {self.core_goal}")
        return self.core_goal
