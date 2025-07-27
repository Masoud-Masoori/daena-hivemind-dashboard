# interrupt_logic.py
class InterruptLogic:
    def __init__(self):
        self.active = False
        self.reason = None

    def trigger(self, reason):
        self.active = True
        self.reason = reason
        print(f"Interrupt triggered due to: {reason}")

    def reset(self):
        self.active = False
        self.reason = None
