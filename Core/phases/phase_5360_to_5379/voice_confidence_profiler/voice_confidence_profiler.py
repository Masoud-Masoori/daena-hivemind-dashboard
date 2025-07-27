# voice_confidence_profiler.py

class VoiceConfidenceProfiler:
    def analyze(self, speech_text, pitch_variance, pauses):
        if pitch_variance < 0.1 and pauses < 2:
            return "High Confidence"
        elif pitch_variance < 0.2:
            return "Moderate Confidence"
        else:
            return "Low Confidence"
