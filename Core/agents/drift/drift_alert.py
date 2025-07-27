def detect_drift(current_behavior, baseline_behavior):
    deviation = abs(len(current_behavior) - len(baseline_behavior))
    return deviation > 2  # Arbitrary threshold
