# adaptive_pace_adjuster.py

import time

class AdaptivePaceAdjuster:
    def __init__(self):
        self.default_pace = 1.0

    def adjust(self, fatigue_level, urgency):
        pace = self.default_pace
        if fatigue_level > 0.5:
            pace *= 0.75
        if urgency > 0.8:
            pace *= 1.25
        return pace
