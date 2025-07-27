def detect_overload(activity_log):
    overload_signals = ["too many threads", "memory spike", "context overflow"]
    for signal in overload_signals:
        if signal in activity_log.lower():
            return True
    return False
