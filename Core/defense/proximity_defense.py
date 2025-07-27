class ProximityDefense:
    def __init__(self, radius):
        self.radius = radius

    def evaluate(self, threat_distance):
        if threat_distance < self.radius:
            return "DEFENSE_TRIGGERED"
        return "CLEAR"
