# action_audit_log.py
from datetime import datetime

class ActionAuditLog:
    def __init__(self):
        self.entries = []

    def log_action(self, agent, action, reason):
        timestamp = datetime.now().isoformat()
        self.entries.append({
            "agent": agent,
            "action": action,
            "reason": reason,
            "timestamp": timestamp
        })
        return f" {agent} -> {action} | Reason: {reason} @ {timestamp}"

    def get_all_logs(self):
        return self.entries
