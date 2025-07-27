# critical_decision_archiver.py

import json, os

def archive_decision(agent_id, decision, reason):
    log_path = f"D:/Ideas/Daena/logs/decisions_{agent_id}.json"
    record = { "decision": decision, "reason": reason }
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f: json.dump([record], f, indent=2)
    else:
        with open(log_path, 'r+') as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=2)
    print(f"[DecisionArchiver]  Decision archived for {agent_id}.")
