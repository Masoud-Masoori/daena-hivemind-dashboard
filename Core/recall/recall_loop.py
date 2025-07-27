class DefenseRecall:
    def __init__(self):
        self.memory_log = []

    def record(self, decision):
        self.memory_log.append(decision)

    def recall_last(self):
        return self.memory_log[-1] if self.memory_log else "NONE"
