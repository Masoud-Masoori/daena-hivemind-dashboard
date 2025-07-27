class GoalReassessor:
    def __init__(self, current_goal, environment):
        self.goal = current_goal
        self.environment = environment

    def reassess(self):
        if "blocker" in self.environment:
            return f"Reassessing goal: {self.goal} due to environment blocker."
        return f"Goal remains valid: {self.goal}"
