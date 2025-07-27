# meta_context_adjuster.py
class MetaContextAdjuster:
    def __init__(self):
        self.context_stack = []

    def update_context(self, message):
        if "change topic" in message.lower():
            self.context_stack.clear()
        else:
            self.context_stack.append(message)
        return self.context_stack[-3:]
