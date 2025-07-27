# tts_fallback_bridge.py
import pyttsx3

class TTSFallback:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        print("[TTSFallback] Using fallback engine...")
        self.engine.say(text)
        self.engine.runAndWait()
