# loop_closer.py
class LoopCloser:
    def __init__(self):
        self.memory = set()

    def check_loop(self, message):
        if message in self.memory:
            return True
        self.memory.add(message)
        return False
