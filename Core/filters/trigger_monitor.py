def monitor_triggers(events):
    count = sum(1 for e in events if "trigger" in e.lower())
    return f"[Guard]  Triggers found: {count}"

if __name__ == "__main__":
    print(monitor_triggers(["Trigger warning", "OK", "No trigger here"]))
