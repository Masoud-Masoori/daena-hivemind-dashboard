class MetaLockState:
    def __init__(self):
        self.locked = True
        self.reason = "Integrity Lock Enabled"

    def unlock(self):
        self.locked = False
        print("Meta-lock disabled.")

    def check(self):
        return self.locked
