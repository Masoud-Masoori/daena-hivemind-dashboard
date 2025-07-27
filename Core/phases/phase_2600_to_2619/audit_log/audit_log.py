# audit_log.py
import json
import os
from datetime import datetime

AUDIT_PATH = "D:/Ideas/Daena/logs/decision_audit.jsonl"

def log_decision(phase, decision, metadata=None):
    os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)
    with open(AUDIT_PATH, 'a') as f:
        record = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "decision": decision,
            "metadata": metadata or {}
        }
        f.write(json.dumps(record) + "\n")
