class InnerMissionTracker:
    def __init__(self):
        self.goals = {}

    def assign_mission(self, agent, mission):
        self.goals[agent] = mission

    def current_mission(self, agent):
        return self.goals.get(agent, " No mission assigned.")
