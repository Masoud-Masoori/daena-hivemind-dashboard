def flag_user_override(decision_point, justification):
    return {
        "override": True,
        "decision_point": decision_point,
        "justification": justification,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }
