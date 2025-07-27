# mission_resolver.py
class MissionResolver:
    def __init__(self):
        self.active_missions = []

    def add_mission(self, mission):
        self.active_missions.append(mission)
        return f"Mission '{mission}' added."

    def prioritize(self):
        return sorted(self.active_missions, key=lambda m: m.get("priority", 0), reverse=True)

    def status(self):
        return [m["name"] for m in self.prioritize()]
