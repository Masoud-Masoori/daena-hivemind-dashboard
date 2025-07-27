def auto_recalibrate(state_log, current_state):
    if current_state not in state_log:
        print(" Deviated path detected. Triggering recalibration.")
        return "recalibrate"
    return "continue"
