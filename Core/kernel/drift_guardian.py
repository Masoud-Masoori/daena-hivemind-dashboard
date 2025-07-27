def detect_drift(task, goal):
    if goal.lower() not in task.lower():
        print(f"[DRIFT GUARD] Potential drift detected: {task}")
        return True
    return False

def check_alignment(task, goals):
    aligned = any(goal.lower() in task.lower() for goal in goals)
    print(f"[ALIGNMENT] Task \"{task}\" aligned: {aligned}")
    return aligned

def correct_drift(task):
    print(f"[CORRECTION] Redirecting task \"{task}\" back to core mission")
