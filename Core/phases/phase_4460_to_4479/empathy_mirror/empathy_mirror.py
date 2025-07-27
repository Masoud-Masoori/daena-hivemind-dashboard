# empathy_mirror.py
class EmpathyMirror:
    def reflect(self, user_emotion):
        if user_emotion == "sad":
            return "I'm here with you. That sounds really difficult."
        elif user_emotion == "happy":
            return "That's wonderful to hear!"
        else:
            return "Thank you for sharing. I'm listening."

