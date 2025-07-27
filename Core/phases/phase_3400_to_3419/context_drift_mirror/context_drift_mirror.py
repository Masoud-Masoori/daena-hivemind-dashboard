# context_drift_mirror.py

history = []

def log_context(context_snapshot):
    history.append(context_snapshot)
    if len(history) > 20:
        history.pop(0)

def detect_drift():
    # Placeholder: implement semantic comparison between early and recent context
    return "Stable" if len(set(history)) < 5 else "Drifting"
