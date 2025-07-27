# auto_voice_handler.py

import threading
from TTS.tts.xtts import speak_text

def speak(text):
    print(f"[Voice AI]  Speaking: {text}")
    thread = threading.Thread(target=speak_text, args=(text,))
    thread.start()
