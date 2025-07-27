### File: core/guards/override_kernel.py

def validate_override(command, context):
    if "shutdown" in command.lower() and "approval" not in context.get("privileges", []):
        return False, " Shutdown command blocked. Insufficient privilege."
    return True, " Command allowed."

def escalate_to_human(command):
    return f"[ESCALATION] Admin review required for: {command}"
