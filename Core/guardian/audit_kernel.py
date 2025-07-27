def audit_trail(logs):
    return [log for log in logs if "unauthorized" in log.lower()]

if __name__ == "__main__":
    logs = ["User authorized", "Unauthorized attempt", "Data synced"]
    print(audit_trail(logs))
