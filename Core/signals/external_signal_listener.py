import time
import random

def listen_to_signal():
    time.sleep(1)
    return random.choice(["ok", "warning", "disconnect"])

if __name__ == "__main__":
    print("[SignalListener] Status:", listen_to_signal())
