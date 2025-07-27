# mission_reminder.py

agent_goals = {}

def set_reminder(agent_id, goal):
    agent_goals[agent_id] = goal
    print(f"[GOAL SET] {agent_id}: {goal}")

def recall_goal(agent_id):
    return agent_goals.get(agent_id, "[NO MISSION FOUND]")

def print_all_goals():
    for agent, goal in agent_goals.items():
        print(f"{agent}: {goal}")
