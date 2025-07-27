class RecoveryFlagPatcher:
    def __init__(self):
        self.flags = {}

    def set_flag(self, point, value=True):
        self.flags[point] = value
        print(f" Recovery flag set at: {point}")

    def check_flag(self, point):
        return self.flags.get(point, False)
