# emotional_resonance_filter.py
import re

class EmotionalResonanceFilter:
    def detect_emotion(self, text):
        emotion_map = {
            "happy": ["great", "love", "amazing"],
            "sad": ["sad", "upset", "depressed"],
            "angry": ["angry", "mad", "furious"],
        }
        for emotion, keywords in emotion_map.items():
            for word in keywords:
                if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                    return emotion
        return "neutral"
