# decision_checker.py
def validate_decision_set(primary, backup, override=None):
    if override:
        return override
    if primary != backup:
        return f"Conflict Detected: Primary='{primary}' vs Backup='{backup}'"
    return primary
