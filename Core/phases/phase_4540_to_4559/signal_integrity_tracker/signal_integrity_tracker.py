# signal_integrity_tracker.py
import hashlib

class SignalIntegrityTracker:
    def __init__(self):
        self.records = {}

    def track(self, message_id, content):
        self.records[message_id] = self._hash(content)

    def verify(self, message_id, content):
        return self.records.get(message_id) == self._hash(content)

    def _hash(self, content):
        return hashlib.sha256(content.encode()).hexdigest()
