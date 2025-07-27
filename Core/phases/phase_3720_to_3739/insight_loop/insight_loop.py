# insight_loop.py
class InsightLoopAmplifier:
    def __init__(self):
        self.memory_window = []

    def process_message(self, msg):
        self.memory_window.append(msg)
        if len(self.memory_window) > 10:
            self.memory_window.pop(0)

    def detect_insight_pattern(self):
        patterns = [m["intent"] for m in self.memory_window]
        return max(set(patterns), key=patterns.count)
