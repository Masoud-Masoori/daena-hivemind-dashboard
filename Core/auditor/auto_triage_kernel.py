class AutoTriage:
    def __init__(self):
        self.history = []

    def log_event(self, event):
        self.history.append(event)
        print("[LOGGED]", event)

    def review_last(self):
        if self.history:
            print("[REVIEW] Returning to last context:", self.history[-1])
        else:
            print("[REVIEW] No prior events to resume.")

if __name__ == '__main__':
    triage = AutoTriage()
    triage.log_event("Voice Module Fix")
    triage.review_last()
