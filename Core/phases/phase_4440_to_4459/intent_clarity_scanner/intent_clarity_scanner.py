# intent_clarity_scanner.py
import re

class IntentClarityScanner:
    def scan(self, message):
        unclear_phrases = re.findall(r"\b(maybe|perhaps|not sure|I think)\b", message, re.IGNORECASE)
        return len(unclear_phrases), unclear_phrases
