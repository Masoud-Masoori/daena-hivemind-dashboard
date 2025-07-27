class RoadmapGuardian:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.last_checkpoint = None

    def update_checkpoint(self, phase):
        self.last_checkpoint = phase

    def return_to_track(self):
        if self.last_checkpoint:
            print(f" Returning to roadmap phase: {self.last_checkpoint}")
            return self.last_checkpoint
