import json
def log_reason(decision, reason):
    with open("D:/Ideas/Daena/logs/rationale_log.jsonl", "a") as f:
        f.write(json.dumps({"decision": decision, "reason": reason}) + "\n")
    print(f"[RATIONALE] Logged: {decision}")
