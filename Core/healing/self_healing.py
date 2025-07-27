class SelfHealingHook:
    def __init__(self):
        self.failures = 0

    def monitor(self, signal):
        if "error" in signal:
            self.failures += 1
            print(" Detected issue. Initiating recovery.")
            return True
        return False

    def reset(self):
        self.failures = 0
