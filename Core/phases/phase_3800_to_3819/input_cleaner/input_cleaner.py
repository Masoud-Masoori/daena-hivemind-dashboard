# input_cleaner.py
import re

class InputCleaner:
    def clean(self, raw_input):
        sanitized = re.sub(r"[^a-zA-Z0-9\s.,?!]", "", raw_input)
        return sanitized.strip()
