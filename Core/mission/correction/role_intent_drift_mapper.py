class RoleIntentDriftMapper:
    def __init__(self):
        self.intents = {}

    def track_intent(self, agent, goal):
        self.intents[agent] = goal
        print(f" {agent} aligned with goal: {goal}")

    def detect_drift(self, agent, new_action):
        expected = self.intents.get(agent, "")
        if expected not in new_action:
            print(f" Drift detected for {agent}: expected '{expected}' but got '{new_action}'")
            return True
        return False
