# Detects major deviations from expected context behavior
def context_watchdog(current_context, baseline):
    diff = set(current_context.items()) - set(baseline.items())
    if diff:
        print(" Context deviation detected:", diff)
    return diff
