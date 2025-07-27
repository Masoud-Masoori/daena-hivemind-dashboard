class PivotAwarenessLayer:
    def __init__(self):
        self.pivots = []

    def register(self, pivot_point):
        print(f" Pivot registered: {pivot_point}")
        self.pivots.append(pivot_point)

    def resume_main_road(self):
        print(" Returning to main goal after pivot.")
