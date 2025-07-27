def monitor_behavior(current, expected):
    if current != expected:
        return f"[DriftMonitor]  Drift detected: {current} vs {expected}"
    return "[DriftMonitor]  Behavior aligned"

if __name__ == "__main__":
    print(monitor_behavior("adaptive", "stable"))
