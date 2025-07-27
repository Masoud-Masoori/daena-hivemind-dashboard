from kernel.drift_detector import check_drift

def guard_action(task):
    if check_drift(task):
        return "[BLOCKED] Task rejected to prevent project drift."
    return "[APPROVED] Task is aligned."
