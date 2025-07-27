class FallbackTracker:
    def __init__(self):
        self.history = []

    def track(self, event):
        self.history.append(event)
        print(f" Tracked: {event}")

    def suggest_return(self):
        if self.history:
            suggestion = self.history[-1]
            print(f" Suggesting return to: {suggestion}")
            return suggestion
        return "No fallback path available."
