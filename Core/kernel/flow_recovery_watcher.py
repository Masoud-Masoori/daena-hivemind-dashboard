def detect_flow_crash(logs):
    for entry in logs:
        if "stalled" in entry or "timeout" in entry:
            print(f"[WATCHER] Flow problem: {entry}")
            return True
    return False
