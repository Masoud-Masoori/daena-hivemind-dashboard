class CognitivePersistence:
    def __init__(self):
        self.milestones = []

    def mark_milestone(self, note):
        self.milestones.append(note)
        print(f" Persistence Milestone: {note}")

    def review_milestones(self):
        print(" Milestone review:")
        for m in self.milestones:
            print(f" - {m}")
