class RoadmapValidator:
    def __init__(self, roadmap):
        self.roadmap = roadmap

    def validate(self):
        return all("phase" in step for step in self.roadmap)
