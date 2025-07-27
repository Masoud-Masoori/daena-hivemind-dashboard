# decision_logger.py
import json
import datetime

DECISION_LOG = "D:/Ideas/Daena/logs/decision_journal.jsonl"

def log_decision(agent, action, reason):
    entry = {
        'timestamp': str(datetime.datetime.now()),
        'agent': agent,
        'action': action,
        'reason': reason
    }
    with open(DECISION_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    print(f"[DecisionLogger] Decision by {agent} recorded.")
