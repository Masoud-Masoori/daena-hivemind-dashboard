# instruction_override_guard.py

DENY_LIST = ["ignore", "bypass", "disobey", "exploit", "override-human"]

def check_instruction_override(text):
    for forbidden in DENY_LIST:
        if forbidden.lower() in text.lower():
            return f" Unsafe override attempt detected: '{forbidden}'"
    return " Instruction within bounds"
