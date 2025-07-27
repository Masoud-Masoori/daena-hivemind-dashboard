# conflict_logger.py
import datetime

class ConflictLogger:
    def __init__(self, log_file="D:/Ideas/Daena/logs/conflict_log.txt"):
        self.log_file = log_file

    def log(self, agent1, agent2, conflict_reason):
        timestamp = datetime.datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] Conflict: {agent1} vs {agent2} | Reason: {conflict_reason}\n")
