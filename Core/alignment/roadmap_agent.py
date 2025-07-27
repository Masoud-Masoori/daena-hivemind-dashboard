class RoadmapAlignmentAgent:
    def __init__(self, roadmap=[]):
        self.roadmap = roadmap
        self.current_index = 0

    def get_next_milestone(self):
        if self.current_index < len(self.roadmap):
            return self.roadmap[self.current_index]
        return " Roadmap completed."

    def advance(self):
        if self.current_index < len(self.roadmap):
            print(f" Reached: {self.roadmap[self.current_index]}")
            self.current_index += 1
