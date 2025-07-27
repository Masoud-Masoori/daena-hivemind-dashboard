# Simulates active context and memory stack control
class CognitiveStack:
    def __init__(self):
        self.stack = []

    def push(self, idea):
        self.stack.append(idea)

    def pop(self):
        return self.stack.pop() if self.stack else None
