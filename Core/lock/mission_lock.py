class MissionLock:
    def __init__(self):
        self.locked = []

    def lock_milestone(self, milestone):
        if milestone not in self.locked:
            self.locked.append(milestone)
            print(f" Milestone locked: {milestone}")
