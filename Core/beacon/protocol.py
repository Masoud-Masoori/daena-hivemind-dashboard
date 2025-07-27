class MissionBeacon:
    def __init__(self, message):
        self.message = message

    def broadcast(self):
        print(f" Mission Beacon: {self.message}")
