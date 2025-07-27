def audit_reactions(actions):
    issues = []
    for idx, act in enumerate(actions):
        if "type" not in act or "timestamp" not in act:
            issues.append(f"Invalid entry at {idx}")
    return issues
