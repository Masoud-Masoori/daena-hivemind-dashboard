# input_filter.py
class InputSanitizer:
    def __init__(self, bad_patterns):
        self.bad_patterns = bad_patterns

    def clean(self, text):
        for p in self.bad_patterns:
            text = text.replace(p, "[REDACTED]")
        return text
