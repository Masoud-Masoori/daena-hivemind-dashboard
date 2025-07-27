current_goals = []

def realign_priorities(task_queue, main_goal):
    global current_goals
    updated_queue = []
    for task in task_queue:
        if main_goal.lower() in task.lower():
            updated_queue.insert(0, task)
        else:
            updated_queue.append(task)
    current_goals = updated_queue
    return updated_queue
