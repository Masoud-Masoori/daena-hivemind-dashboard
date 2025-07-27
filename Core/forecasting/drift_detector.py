def detect_drift(current, baseline):
    diff = abs(current - baseline)
    return f"[DriftDetector]  Drift Detected: {diff}" if diff > 0.5 else "[Stable] "

if __name__ == "__main__":
    print(detect_drift(0.92, 0.3))
