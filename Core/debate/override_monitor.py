def monitor_override(log):
    return [entry for entry in log if entry["overridden"]]

if __name__ == "__main__":
    log = [{"id": 1, "overridden": False}, {"id": 2, "overridden": True}]
    print("[Overrides] :", monitor_override(log))
