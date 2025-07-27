# focus_persistence.py
class FocusPersistence:
    def __init__(self):
        self.memory_stack = []

    def push_context(self, context):
        self.memory_stack.append(context)

    def pop_context(self):
        return self.memory_stack.pop() if self.memory_stack else None

    def resume_last_context(self):
        return self.memory_stack[-1] if self.memory_stack else None
