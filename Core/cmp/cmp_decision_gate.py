import json
import os
from datetime import datetime

def verify_risk(decision):
    high_risk_keywords = ["spend", "transfer", "sign", "invest"]
    if any(word in decision.lower() for word in high_risk_keywords):
        log_decision(decision, "rejected")
        print("[CMP] Confirm with Masoud before executing this decision.")
        return False
    log_decision(decision, "accepted")
    return True

def log_decision(decision, status):
    log_dir = "D:/Ideas/Daena/logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "decisions.log"), "a") as f:
        f.write(f"{datetime.now()} | {status} | {decision}\n")
