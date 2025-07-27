def detect_drift(tracked, current):
    drift = list(set(current) - set(tracked))
    return f"[DriftSensor]  Drift Detected: {drift}" if drift else "[DriftSensor]  Stable"

if __name__ == "__main__":
    print(detect_drift(["lawful", "ethical"], ["lawful", "rogue"]))
