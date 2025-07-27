# roadmap_recenter.py
class RoadmapRecenter:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.current_step = 0

    def reset_to_last_checkpoint(self):
        return f" Returning to checkpoint at step {self.current_step}"

    def advance(self):
        self.current_step += 1
        return f" Proceeding to step {self.current_step}"

    def status(self):
        return f" Currently at roadmap step {self.current_step}"
