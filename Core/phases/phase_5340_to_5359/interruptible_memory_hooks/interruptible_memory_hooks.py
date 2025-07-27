# interruptible_memory_hooks.py

class InterruptibleMemoryHooks:
    def __init__(self):
        self.pending_memories = []

    def queue(self, memory_fragment, confidence):
        if confidence >= 0.7:
            return "Auto-stored: Confidence high."
        else:
            self.pending_memories.append(memory_fragment)
            return "Held for review: Confidence low."

    def review_pending(self):
        return self.pending_memories
