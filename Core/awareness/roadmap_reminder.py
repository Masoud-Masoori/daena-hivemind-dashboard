class RoadmapReminder:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.pointer = 0

    def current_target(self):
        if self.pointer < len(self.roadmap):
            return self.roadmap[self.pointer]
        return " All goals completed."

    def advance(self):
        if self.pointer < len(self.roadmap) - 1:
            self.pointer += 1
            print(f" Advanced to: {self.roadmap[self.pointer]}")

    def remind(self):
        print(f" Stay on track: Next goal  {self.current_target()}")
