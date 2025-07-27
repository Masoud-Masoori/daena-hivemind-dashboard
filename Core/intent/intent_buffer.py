class IntentBuffer:
    def __init__(self):
        self.buffer = []

    def push(self, intent):
        self.buffer.append(intent)

    def pop(self):
        return self.buffer.pop(0) if self.buffer else None

    def clear(self):
        self.buffer.clear()
