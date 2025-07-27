import speech_recognition as sr
from tts.xtts_loader import daena_speak
from core.context import VoiceContext
from core.intent_dispatcher import dispatch_intent
import time
import logging

WAKE_WORD = "daena"
context = VoiceContext()

logging.basicConfig(filename="D:/Ideas/Daena/logs/voice_log.txt", level=logging.INFO)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Daena Listener]  Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        logging.warning(" Could not understand audio.")
        return ""
    except sr.RequestError as e:
        logging.error(f" API error: {e}")
        return ""

def wake_loop():
    print("[Daena Listener]  Wake loop active.")
    while True:
        heard = recognize_speech()
        if WAKE_WORD in heard:
            logging.info(f" Wake word heard: {heard}")
            daena_speak("Yes, I'm here. How can I help?")
            context.record(heard)

            command = recognize_speech()
            if command:
                daena_speak(f"Executing: {command}")
                dispatch_intent(command)
