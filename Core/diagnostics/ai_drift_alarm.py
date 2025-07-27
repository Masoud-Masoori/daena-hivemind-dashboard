class AIDriftAlarm:
    def __init__(self, threshold=0.4):
        self.threshold = threshold

    def check_alignment(self, current_state, expected_state):
        drift = abs(current_state - expected_state)
        if drift > self.threshold:
            print(" AI alignment drift detected!")
            return True
        return False
