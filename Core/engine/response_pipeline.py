# response_pipeline.py
from core.engine.loop_control import detect_loop
from core.engine.hallucination_filter import is_hallucination
from core.engine.emotion_filter import apply_emotion

def process_response(response, emotion="neutral"):
    if detect_loop(response):
        return "[Loop Detected]  Repeating response blocked."
    if is_hallucination(response):
        return "[Filtered]  Potential hallucination removed."
    return apply_emotion(response, emotion)
