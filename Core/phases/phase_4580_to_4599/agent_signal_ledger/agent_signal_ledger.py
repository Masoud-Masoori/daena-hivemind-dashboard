# agent_signal_ledger.py
import time

class AgentSignalLedger:
    def __init__(self):
        self.ledger = []

    def log_signal(self, sender, receiver, message):
        timestamp = time.time()
        entry = {"from": sender, "to": receiver, "msg": message, "time": timestamp}
        self.ledger.append(entry)
        return entry
