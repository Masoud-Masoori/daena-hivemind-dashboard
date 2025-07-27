def check_ledger_consistency(log_entries):
    conflicts = [entry for entry in log_entries if "override" in entry.get("reason", "").lower()]
    return len(conflicts) == 0
