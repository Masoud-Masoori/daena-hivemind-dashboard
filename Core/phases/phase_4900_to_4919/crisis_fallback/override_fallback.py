# override_fallback.py
class CrisisFallback:
    def __init__(self):
        self.last_known_safe_state = None

    def activate(self, reason):
        print(f" Fallback Activated due to: {reason}")
        return self.last_known_safe_state or "Minimal safe-mode activated"
