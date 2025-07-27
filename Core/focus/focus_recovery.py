def recursive_focus(tasks, goal):
    focus_path = []
    for t in tasks:
        if goal in t:
            focus_path.append(t)
    return focus_path if focus_path else ["Redirect to: " + goal]
