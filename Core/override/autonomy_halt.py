def autonomous_halt_trigger(state_report):
    if "unstable" in state_report.lower():
        print("Autonomy suspended pending review.")
        return True
    return False
