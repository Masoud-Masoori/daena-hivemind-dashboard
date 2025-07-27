# adaptive_politeness_handler.py
class AdaptivePolitenessHandler:
    def adjust_tone(self, message, emotion):
        if emotion == "angry":
            return "I understand you're upset. Let's resolve this together: " + message
        elif emotion == "sad":
            return "I'm here for you. " + message
        return message
