# fireline_gatekeeper.py
class FirelineGatekeeper:
    def __init__(self, danger_threshold=0.9):
        self.threshold = danger_threshold

    def evaluate_risk(self, score):
        if score >= self.threshold:
            print(f"[FirelineGatekeeper]  Risk score {score} exceeded threshold!")
            return "BLOCK"
        print(f"[FirelineGatekeeper] Risk score {score} is within safe bounds.")
        return "ALLOW"
