def suggest_override(agent, context):
    print(f"[SuggestionOverlay]  Reviewing actions for: {agent}")
    if "repeat" in context.lower() or "again" in context.lower():
        return f" Oversight Suggestion: {agent} may be repeating logic."
    return None
