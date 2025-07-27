class DistractionShield:
    def __init__(self, blacklist):
        self.blacklist = blacklist

    def check(self, signal):
        return any(trigger in signal.lower() for trigger in self.blacklist)
