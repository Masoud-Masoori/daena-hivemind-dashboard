# emotion_detector.py
import re

class EmotionDetector:
    def detect(self, text):
        emotions = {"happy": ["joy", "glad", "awesome"], "sad": ["down", "blue", "upset"], "angry": ["mad", "furious", "annoyed"]}
        for label, keywords in emotions.items():
            for word in keywords:
                if re.search(rf"\\b{word}\\b", text, re.IGNORECASE):
                    return label
        return "neutral"
