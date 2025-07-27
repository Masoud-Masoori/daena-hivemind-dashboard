# goal_tracker.py
class GoalTracker:
    def __init__(self, main_goal):
        self.main_goal = main_goal
        self.progress = []

    def log_step(self, description):
        self.progress.append(description)

    def get_status(self):
        return {
            "goal": self.main_goal,
            "steps_logged": len(self.progress),
            "log": self.progress
        }
