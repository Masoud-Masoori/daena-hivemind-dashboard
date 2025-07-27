# trigger_enforcer.py
def enforce_trigger(signal, allowed=["EMERGENCY", "BLOCK", "ESCALATE"]):
    return signal.upper() in allowed
