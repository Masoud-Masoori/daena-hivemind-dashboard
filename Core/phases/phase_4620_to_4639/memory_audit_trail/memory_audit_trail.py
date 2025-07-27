# memory_audit_trail.py
import json
import time

class MemoryAuditTrail:
    def __init__(self, log_path="D:/Ideas/Daena/audit/memory_log.jsonl"):
        self.log_path = log_path

    def log_event(self, agent, event_type, content):
        with open(self.log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": time.time(),
                "agent": agent,
                "type": event_type,
                "content": content
            }) + "\n")
