# memory_refinement.py
class MemoryRefinementProtocol:
    def __init__(self, memory_buffer):
        self.buffer = memory_buffer

    def purge_noise(self):
        self.buffer = [entry for entry in self.buffer if entry["confidence"] >= 0.7]

    def compress_context(self):
        return " ".join(entry["text"] for entry in self.buffer)
