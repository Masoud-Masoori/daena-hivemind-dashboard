# priority_drift.py
def check_drift(current_priority, roadmap_priority):
    if current_priority != roadmap_priority:
        print(f"[Drift Warning] Current='{current_priority}' vs Roadmap='{roadmap_priority}'")
        return True
    return False
