class DefenseBeacon:
    def __init__(self):
        self.status = "IDLE"

    def activate(self, level):
        self.status = f"BEACON-LEVEL-{level}"
        print(f" Defense Beacon Activated at {self.status}")
