# gatekeeper_monitor.py
import datetime

class GatekeeperMonitor:
    def __init__(self):
        self.logs = []

    def log_event(self, agent_id, action, result):
        self.logs.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "result": result
        })

    def get_logs(self):
        return self.logs
