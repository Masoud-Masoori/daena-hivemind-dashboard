# reset_verifier.py
class ResetVerifier:
    def __init__(self):
        self.reset_log = []

    def verify_integrity_post_reset(self, status):
        self.reset_log.append(status)
        if status == "OK":
            return True
        return False
