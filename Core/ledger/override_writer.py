import json
import os

def write_override_log(agent_id, action, reason):
    log = {
        "agent": agent_id,
        "action": action,
        "reason": reason
    }
    log_path = "D:/Ideas/Daena/core/ledger/override_log.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(log) + "\n")
    print(f"Logged override by {agent_id}")
