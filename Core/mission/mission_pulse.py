def mission_pulse_check(agent_log):
    if "deviation" in agent_log:
        print(" Mission deviation detected.")
        return "realign_to_objectives"
    return "on_track"
