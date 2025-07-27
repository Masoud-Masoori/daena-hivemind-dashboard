dream_loop_control.py
import time

seen = set()
def detect_loop(key):
    if key in seen:
        print("[Loop Guard] 🚫 Loop detected:", key)
        return True
    seen.add(key)
    return False