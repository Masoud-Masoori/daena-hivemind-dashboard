# dynamic_tone_engine.py
class DynamicToneEngine:
    def __init__(self):
        self.current_tone = "neutral"

    def update_tone(self, mood):
        if mood in ["happy", "inspired"]:
            self.current_tone = "cheerful"
        elif mood in ["sad", "tired"]:
            self.current_tone = "calm"
        elif mood in ["angry", "frustrated"]:
            self.current_tone = "assertive"
        else:
            self.current_tone = "neutral"

    def get_tone(self):
        return self.current_tone
