def inspect_triggers(events):
    return [f"[Trigger]  {e}" for e in events if "trigger" in e.lower()]

if __name__ == "__main__":
    print(inspect_triggers(["on_start", "trigger_alert", "manual_override"]))
