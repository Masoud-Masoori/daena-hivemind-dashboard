class FocusWatchdog:
    def __init__(self, focus_criteria):
        self.criteria = focus_criteria

    def detect_loss(self, current):
        if current not in self.criteria:
            print(" Focus lost. Triggering redirect.")
            return True
        return False
