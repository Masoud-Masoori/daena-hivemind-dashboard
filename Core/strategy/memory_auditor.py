def audit_memory(logs):
    errors = [log for log in logs if "error" in log.lower()]
    return f"[Audit]  {len(errors)} error(s) detected." if errors else "[Audit]  All clear."

if __name__ == "__main__":
    print(audit_memory(["Task started", "Connection error", "Retry successful"]))
