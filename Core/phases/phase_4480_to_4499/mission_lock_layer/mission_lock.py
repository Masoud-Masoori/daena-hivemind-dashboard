# mission_lock.py
class MissionLockLayer:
    def __init__(self, mission):
        self.active_mission = mission
        self.locked = True

    def validate_action(self, action_tag):
        return self.locked and action_tag in self.active_mission["allowed_tags"]
