# goal_reprioritizer.py
import json

GOALS_FILE = "D:/Ideas/Daena/memory/mission_goals.json"

def reprioritize_goals(high_priority):
    with open(GOALS_FILE, 'r') as f:
        goals = json.load(f)
    prioritized = sorted(goals, key=lambda g: g['name'] != high_priority)
    with open(GOALS_FILE, 'w') as f:
        json.dump(prioritized, f, indent=2)
    print(f"[GoalReprioritizer] Focused on: {high_priority}")
