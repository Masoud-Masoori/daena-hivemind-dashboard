class FocusLock:
    def __init__(self):
        self.last_intended = None
        self.last_diversion = None

    def set_intended_goal(self, goal):
        self.last_intended = goal

    def mark_diversion(self, where):
        self.last_diversion = where

    def report(self):
        return f"Last goal: {self.last_intended}, diverted at: {self.last_diversion}"
