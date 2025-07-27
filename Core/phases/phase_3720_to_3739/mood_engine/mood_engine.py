# mood_engine.py
class AIMoodEngine:
    def __init__(self):
        self.mood = "neutral"

    def update_mood(self, sentiment_score):
        if sentiment_score > 0.7:
            self.mood = "positive"
        elif sentiment_score < 0.3:
            self.mood = "concerned"
        else:
            self.mood = "neutral"

    def get_voice_style(self):
        return {
            "positive": "cheerful",
            "concerned": "calm",
            "neutral": "warm"
        }.get(self.mood, "warm")
