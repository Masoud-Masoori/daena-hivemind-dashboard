def context_resolver(conflict):
    context = conflict.get("context", "")
    if "emergency" in context:
        return "Handle as critical"
    return None
