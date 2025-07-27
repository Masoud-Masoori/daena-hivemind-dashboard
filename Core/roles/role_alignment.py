### File: core/roles/role_alignment.py

def get_role_behavior(role):
    presets = {
        "assistant": {
            "tone": "warm",
            "verbosity": "medium",
            "decision_privilege": "medium"
        },
        "department_head": {
            "tone": "directive",
            "verbosity": "low",
            "decision_privilege": "high"
        },
        "hidden_agent": {
            "tone": "discreet",
            "verbosity": "minimal",
            "decision_privilege": "guarded"
        }
    }
    return presets.get(role, presets["assistant"])
