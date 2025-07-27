from core.filter.hallucination_filter import detect_hallucination
from core.loop_guard.dream_loop_control import detect_loop
from core.emotion.emotional_regulator import regulate_emotion

def validate_output(text, history, emotion="calm"):
    if detect_loop(text):
        return "[Loop halted]"
    if detect_hallucination(text, history):
        return "[Filtered: hallucination]"
    return regulate_emotion(text, emotion)
