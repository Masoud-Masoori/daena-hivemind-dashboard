# Expands micro-decisions using localized heuristics
def expand_locally(decision):
    return [decision] + [f"{decision}_fallback", f"{decision}_escalate"]
