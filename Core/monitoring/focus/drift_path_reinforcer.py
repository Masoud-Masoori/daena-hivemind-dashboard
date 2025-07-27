class DriftPathReinforcer:
    def __init__(self, path_reminder):
        self.reminder = path_reminder

    def reinforce(self):
        print(f" Re-aligning with: {self.reminder}")
