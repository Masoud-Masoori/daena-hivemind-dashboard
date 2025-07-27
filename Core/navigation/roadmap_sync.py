class RoadmapSync:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.current_focus = None

    def sync(self, focus):
        if focus in self.roadmap:
            self.current_focus = focus
            print(f" Synced to: {focus}")
        else:
            print(" Focus not in roadmap.")

    def status(self):
        return f" Current focus: {self.current_focus}"
