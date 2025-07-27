# drift_recovery_engine.py
class DriftRecoveryEngine:
    def __init__(self):
        self.interrupt_stack = []

    def mark_interrupt(self, task, reason):
        self.interrupt_stack.append((task, reason))

    def resume_last_task(self):
        return self.interrupt_stack.pop() if self.interrupt_stack else None
