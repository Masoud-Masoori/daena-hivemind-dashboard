def realign_decision_path(decision_history):
    if not decision_history:
        return []
    aligned = [d for d in decision_history if d.get("valid", True)]
    return aligned
