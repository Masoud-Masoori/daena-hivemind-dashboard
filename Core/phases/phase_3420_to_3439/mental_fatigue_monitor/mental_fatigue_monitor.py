# mental_fatigue_monitor.py

recent_decisions = []

def monitor_decision(decision):
    recent_decisions.append(decision)
    if len(recent_decisions) > 20:
        recent_decisions.pop(0)

def detect_loop():
    return len(set(recent_decisions)) < 5
