# thought_traceback.py
class ThoughtTraceback:
    def __init__(self):
        self.thought_chain = []

    def log(self, reason, inputs):
        self.thought_chain.append({"reason": reason, "inputs": inputs})

    def trace(self):
        return self.thought_chain
