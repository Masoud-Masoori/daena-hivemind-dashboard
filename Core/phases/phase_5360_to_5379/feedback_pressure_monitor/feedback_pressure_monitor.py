# feedback_pressure_monitor.py

class FeedbackPressureMonitor:
    def evaluate(self, feedback_list):
        intensity = sum(1 for fb in feedback_list if "!" in fb or len(fb) > 80)
        if intensity > 5:
            return "High Pressure"
        elif intensity > 2:
            return "Moderate Pressure"
        return "Low Pressure"
