# semantic_drift_detector.py

def detect_drift(old_context, new_context):
    drift_score = sum(1 for k in old_context if k in new_context and old_context[k] != new_context[k])
    normalized_score = drift_score / max(len(old_context), 1)
    print(f"[DriftDetector]  Drift score: {normalized_score:.2f}")
    return normalized_score
