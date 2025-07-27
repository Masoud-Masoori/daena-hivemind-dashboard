class MemoryRing:
    def __init__(self, size=5):
        self.size = size
        self.buffer = []

    def remember(self, item):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(item)

    def recall(self):
        return self.buffer

if __name__ == "__main__":
    m = MemoryRing()
    for i in range(7):
        m.remember(f"Thought {i}")
    print("[MemoryRing]  Buffer:", m.recall())
