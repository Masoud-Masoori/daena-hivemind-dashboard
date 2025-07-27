# emotion_feedback_balancer.py
class EmotionFeedbackBalancer:
    def __init__(self):
        self.emotion_scores = []

    def add_emotion_feedback(self, emotion_score):
        self.emotion_scores.append(emotion_score)

    def get_balance_level(self):
        if not self.emotion_scores:
            return 0.0
        return sum(self.emotion_scores) / len(self.emotion_scores)
