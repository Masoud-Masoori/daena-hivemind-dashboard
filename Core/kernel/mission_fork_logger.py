def log_fork(reason):
    from datetime import datetime
    entry = {"timestamp": datetime.now().isoformat(), "reason": reason}
    print(f"[FORK] {reason}")
    with open("D:/Ideas/Daena/logs/fork_events.jsonl", "a") as f:
        f.write(str(entry) + "\n")
