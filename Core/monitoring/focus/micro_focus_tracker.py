class MicroFocusTracker:
    def __init__(self):
        self.subtasks = {}

    def track(self, subtask, focus_score):
        self.subtasks[subtask] = focus_score

    def is_drifting(self):
        return any(score < 0.5 for score in self.subtasks.values())
