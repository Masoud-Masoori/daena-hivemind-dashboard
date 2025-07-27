class MomentumGuard:
    def __init__(self):
        self.flags = []

    def raise_flag(self, reason):
        self.flags.append(reason)

    def is_clear(self):
        return len(self.flags) == 0
