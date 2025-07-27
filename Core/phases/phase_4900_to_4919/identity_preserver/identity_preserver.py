# identity_preserver.py
import hashlib

class IdentityPreserver:
    def __init__(self, fingerprint="Daena-Core"):
        self.fingerprint = fingerprint
        self.hash = self._compute_hash()

    def _compute_hash(self):
        return hashlib.sha256(self.fingerprint.encode()).hexdigest()

    def verify(self):
        return self._compute_hash() == self.hash
