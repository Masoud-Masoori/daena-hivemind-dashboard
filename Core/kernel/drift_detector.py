from kernel.goal_anchor import get_goal

def check_drift(task):
    goal = get_goal()
    if any(word in task.lower() for word in goal.lower().split()):
        return False  # aligned
    print(f"[DRIFT] Task '{task}' may not support goal: '{goal}'")
    return True
