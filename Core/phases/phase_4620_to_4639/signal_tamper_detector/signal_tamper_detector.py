# signal_tamper_detector.py
import hashlib

class SignalTamperDetector:
    def __init__(self):
        self.signatures = {}

    def register(self, signal_id, content):
        self.signatures[signal_id] = hashlib.sha256(content.encode()).hexdigest()

    def verify(self, signal_id, content):
        new_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.signatures.get(signal_id) == new_hash
