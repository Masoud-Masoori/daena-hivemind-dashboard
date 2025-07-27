# chat_safety_loop.py
class ChatSafetyLoop:
    def __init__(self):
        self.blocked_words = ["self-harm", "violence", "fake news", "illegal"]

    def scan_response(self, text):
        for word in self.blocked_words:
            if word in text.lower():
                print(f"[ChatSafetyLoop] Blocked term found: {word}")
                return False
        return True
