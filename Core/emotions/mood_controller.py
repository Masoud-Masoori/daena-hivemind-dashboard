class MoodController:
    def __init__(self):
        self.mood = "neutral"

    def update_mood(self, feedback_score):
        if feedback_score > 0.6:
            self.mood = "positive"
        elif feedback_score < 0.3:
            self.mood = "concerned"
        else:
            self.mood = "neutral"
        return self.mood
