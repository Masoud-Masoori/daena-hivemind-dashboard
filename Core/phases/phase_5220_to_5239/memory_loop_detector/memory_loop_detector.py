# memory_loop_detector.py
class MemoryLoopDetector:
    def __init__(self):
        self.last_inputs = []

    def detect_loop(self, current_input):
        self.last_inputs.append(current_input)
        if len(self.last_inputs) > 5:
            self.last_inputs.pop(0)
        return self.last_inputs.count(current_input) > 2
