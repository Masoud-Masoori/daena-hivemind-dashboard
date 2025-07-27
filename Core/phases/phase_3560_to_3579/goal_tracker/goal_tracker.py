# goal_tracker.py
global_roadmap = ["Launch Daena", "Voice Stability", "LLM Sync", "HiveOS", "Global Agent Expansion"]

def current_goal_index(status_report):
    for i, goal in enumerate(global_roadmap):
        if goal not in status_report["completed_goals"]:
            return i
    return len(global_roadmap)
