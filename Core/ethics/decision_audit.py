import datetime
def log_decision(action, outcome):
    now = datetime.datetime.now().isoformat()
    return f"[AUDIT] {now} - Action: {action} => Outcome: {outcome}"

if __name__ == "__main__":
    print(log_decision("override_limit", "approved"))
