import time
import json
from datetime import datetime

def log_metrics(metrics):
    with open("D:/Ideas/Daena/logs/monitoring_log.jsonl", "a") as f:
        entry = {"timestamp": datetime.utcnow().isoformat(), **metrics}
        f.write(json.dumps(entry) + "\n")
    print(f"[MONITOR] Logged metrics at {entry['timestamp']}")

def daemon_cycle():
    while True:
        # Example metrics
        metrics = {
            "active_agents": 10,
            "tasks_completed": 42,
            "departments_active": 5,
            "sla_compliance": 0.95,
            "drift_events": 0
        }
        log_metrics(metrics)
        time.sleep(30)  # Log every 30 seconds

if __name__ == "__main__":
    daemon_cycle()
