class BacktrackMarker:
    def __init__(self):
        self.stack = []

    def mark(self, phase):
        self.stack.append(phase)

    def go_back(self):
        if self.stack:
            last = self.stack.pop()
            print(f" Backtracked to phase: {last}")
            return last
        return None
