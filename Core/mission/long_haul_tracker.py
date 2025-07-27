class LongHaulTracker:
    def __init__(self):
        self.roadmap = []
    
    def add_milestone(self, phase, objective):
        self.roadmap.append({"phase": phase, "objective": objective})
        print(f" Added milestone: {phase}  {objective}")

    def progress_summary(self):
        print(" Long-haul tracking active:")
        return self.roadmap
