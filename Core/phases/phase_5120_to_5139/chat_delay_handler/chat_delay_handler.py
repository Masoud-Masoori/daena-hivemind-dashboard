# chat_delay_handler.py
import time

class ChatDelayHandler:
    def respond_with_delay(self, text, delay=1.0):
        time.sleep(delay)
        return text
