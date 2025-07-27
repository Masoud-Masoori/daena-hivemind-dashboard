def should_override(response, user_memory):
    for flag in user_memory.get("overrides", []):
        if flag in response:
            return True
    return False
