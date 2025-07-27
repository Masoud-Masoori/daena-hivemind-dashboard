# pattern_disruptor.py
from collections import deque

class PatternDetector:
    def __init__(self, window=5):
        self.window = window
        self.history = deque(maxlen=window)

    def add_action(self, action):
        self.history.append(action)

    def detect_loop(self):
        return len(set(self.history)) == 1 if len(self.history) == self.window else False
