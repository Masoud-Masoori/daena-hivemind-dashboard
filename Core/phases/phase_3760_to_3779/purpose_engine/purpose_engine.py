# purpose_engine.py
class PurposeEngine:
    def __init__(self, mission="Support Masoud's vision"):
        self.mission = mission
        self.current_focus = None

    def evaluate_action(self, action):
        if self.mission.lower() in action.lower():
            return "Aligned"
        return "Off-track"

    def update_focus(self, focus):
        self.current_focus = focus
