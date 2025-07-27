def detect_conflict(signal_a, signal_b):
    if signal_a == "go" and signal_b == "stop":
        return True
    return False
