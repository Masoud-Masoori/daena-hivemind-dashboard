# humor_detection_agent.py

import re

class HumorDetectionAgent:
    def detect(self, text):
        keywords = ["joke", "funny", "hilarious", "lol", "lmao", ":)", ""]
        if any(k in text.lower() for k in keywords):
            return True
        if re.search(r"\blol\b|\blmao\b", text, re.IGNORECASE):
            return True
        return False
