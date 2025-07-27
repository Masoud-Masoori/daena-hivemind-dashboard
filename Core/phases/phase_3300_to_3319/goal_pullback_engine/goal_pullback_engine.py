# goal_pullback_engine.py

agent_goals = {}

def set_goal(agent_id, goal):
    agent_goals[agent_id] = goal

def pull_back(agent_id):
    goal = agent_goals.get(agent_id)
    if goal:
        print(f"[PULLBACK] {agent_id} re-aligning to goal: {goal}")
        return goal
    else:
        print(f"[NO GOAL] {agent_id} has no set goal.")
        return None
