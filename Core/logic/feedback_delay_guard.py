import time

def guard_feedback_loop(delay=1.0):
    print("[LoopGuard]  Waiting...")
    time.sleep(delay)
    return "[LoopGuard]  Safe to continue"

if __name__ == "__main__":
    print(guard_feedback_loop())
