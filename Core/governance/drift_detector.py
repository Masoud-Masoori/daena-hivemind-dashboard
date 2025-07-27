def detect_drift(current, baseline):
    if current != baseline:
        return f"[DriftAlert]  Decision drift detected! Current: {current}, Baseline: {baseline}"
    return "[DriftAlert]  Stable decision logic"

if __name__ == "__main__":
    print(detect_drift("use_model_A", "use_model_B"))
