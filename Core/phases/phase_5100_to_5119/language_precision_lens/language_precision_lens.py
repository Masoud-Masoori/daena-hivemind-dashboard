# language_precision_lens.py
import re

class LanguageLens:
    def __init__(self):
        self.corrections = []

    def refine(self, text):
        corrected = re.sub(r"\b(aint|gonna|wanna)\b", "going to", text, flags=re.IGNORECASE)
        if corrected != text:
            self.corrections.append((text, corrected))
        return corrected
