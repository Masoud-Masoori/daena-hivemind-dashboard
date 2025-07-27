# drift_monitor.py

class MentalDriftMonitor:
    def __init__(self):
        self.focus_index = {}

    def check_drift(self, agent_id, current_goal, current_activity):
        if current_goal not in current_activity:
            print(f"[DriftMonitor]  Drift detected for {agent_id}! Refocusing on goal: {current_goal}")
            return True
        return False
