class GoalLockMatrix:
    def __init__(self, goal):
        self.locked_goal = goal

    def enforce(self):
        print(f" Staying focused on: {self.locked_goal}")
