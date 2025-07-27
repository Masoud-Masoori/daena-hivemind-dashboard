goal_log = []

def add_goal(goal):
    goal_log.append(goal)
    return f"[GoalTrack]  Added: {goal}"

def recent_goals(n=3):
    return goal_log[-n:]

if __name__ == "__main__":
    add_goal("Launch version 10")
    add_goal("Sync agent logs")
    print(recent_goals())
