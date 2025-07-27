# emotional_stability_tracker.py

class EmotionalStabilityTracker:
    def __init__(self):
        self.mood_levels = []

    def record_mood(self, score):
        self.mood_levels.append(score)
        return self.is_stable()

    def is_stable(self):
        if len(self.mood_levels) < 3:
            return True
        return abs(self.mood_levels[-1] - self.mood_levels[-2]) < 0.3
