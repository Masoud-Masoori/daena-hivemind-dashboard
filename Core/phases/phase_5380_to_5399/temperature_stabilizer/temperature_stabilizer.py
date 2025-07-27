# temperature_stabilizer.py

class DecisionTemperatureStabilizer:
    def __init__(self):
        self.current_temp = 0.8

    def adjust(self, user_stress_level, task_urgency):
        if user_stress_level > 7 or task_urgency > 7:
            self.current_temp = 0.4
        elif user_stress_level < 3 and task_urgency < 3:
            self.current_temp = 1.0
        else:
            self.current_temp = 0.7
        return self.current_temp
