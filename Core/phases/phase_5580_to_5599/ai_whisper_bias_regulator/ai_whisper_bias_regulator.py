# ai_whisper_bias_regulator.py

class AIWhisperBiasRegulator:
    def __init__(self):
        self.suspect_phrases = ["you should", "definitely", "always", "never"]

    def check_bias(self, message):
        return any(phrase in message.lower() for phrase in self.suspect_phrases)

    def report_if_biased(self, message):
        if self.check_bias(message):
            return " Bias detected in LLM response."
        return " Message is neutral."
