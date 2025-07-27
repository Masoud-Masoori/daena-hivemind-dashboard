class PivotMemory:
    def __init__(self):
        self.pivot_points = []

    def record_pivot(self, reason, state):
        self.pivot_points.append({"reason": reason, "state": state})
        print(" Pivot recorded:", reason)

    def list_pivots(self):
        return self.pivot_points
