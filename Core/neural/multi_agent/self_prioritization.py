def prioritize_goals(agent_goals):
    sorted_goals = sorted(agent_goals, key=lambda g: g["urgency"], reverse=True)
    return sorted_goals

if __name__ == "__main__":
    goals = [{"task": "debug", "urgency": 3}, {"task": "reply email", "urgency": 1}]
    print("[Prioritize] ", prioritize_goals(goals))
