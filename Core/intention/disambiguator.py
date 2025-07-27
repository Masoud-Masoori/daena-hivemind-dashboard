# File: core/intention/disambiguator.py
def clarify_intent(user_input):
    if "schedule" in user_input.lower():
        return "calendar"
    elif "buy" in user_input.lower():
        return "commerce"
    elif "fix" in user_input.lower():
        return "support"
    return "general"
