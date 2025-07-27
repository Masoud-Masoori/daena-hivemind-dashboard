# ux_pain_sensor.py

class UXPainSensor:
    def __init__(self):
        self.pain_log = []

    def detect_friction(self, input_latency, error_rate):
        if input_latency > 2.0 or error_rate > 0.05:
            self.pain_log.append((input_latency, error_rate))
            return True
        return False
