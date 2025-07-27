class AnalyticsPulse:
    def __init__(self):
        self.metrics = []

    def track(self, label, value):
        self.metrics.append((label, value))

    def summarize(self):
        print(" Analytics Summary:")
        for m in self.metrics:
            print(f" - {m[0]}: {m[1]}")
