class MissionRecallAgent:
    def __init__(self, primary_goal="launch_daena"):
        self.goal = primary_goal

    def recall(self):
        print(f" Recalling mission: {self.goal}")
        return self.goal
