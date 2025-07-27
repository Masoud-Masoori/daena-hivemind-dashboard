def check_alignment(task, goals):
    aligned = any(goal.lower() in task.lower() for goal in goals)
    print(f"[ALIGNMENT] Task \"{task}\" aligned: {aligned}")
    return aligned
