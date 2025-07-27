def choose_recovery_action(issue_type):
    recovery_map = {
        "drift": "realign_behavior()",
        "conflict": "reassess_goals()",
        "failure": "rollback_state()"
    }
    return recovery_map.get(issue_type, "manual_review()")
