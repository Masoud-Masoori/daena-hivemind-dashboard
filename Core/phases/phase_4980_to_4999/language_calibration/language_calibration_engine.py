# language_calibration_engine.py
import re

class LanguageCalibrationEngine:
    def clean_text(self, text):
        return re.sub(r"\s+", " ", text.strip())

    def calibrate(self, message, level="professional"):
        if level == "friendly":
            return f"Hey! {message}"
        elif level == "formal":
            return f"Dear user, {message}"
        return message
