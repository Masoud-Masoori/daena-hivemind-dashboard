# input_stream_normalizer.py
import re

class InputStreamNormalizer:
    def normalize(self, text):
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("...", "")
        return text
