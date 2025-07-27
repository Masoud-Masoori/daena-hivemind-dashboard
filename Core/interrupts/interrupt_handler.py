class InterruptHandler:
    def __init__(self):
        self.paused = False
        self.context_stack = []

    def trigger_pause(self, reason="Manual"):
        self.paused = True
        print(f"[INTERRUPT] Paused due to: {reason}")
        self.context_stack.append(reason)

    def resume(self):
        if self.paused:
            reason = self.context_stack.pop() if self.context_stack else "Unknown"
            print(f"[RESUME] Resuming from: {reason}")
            self.paused = False
        else:
            print("[INFO] Already running.")
