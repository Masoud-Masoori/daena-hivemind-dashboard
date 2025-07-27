# timekeeper.py
import time
import threading

def start_timekeeper(log_path="D:/Ideas/Daena/core/logs/time_log.txt"):
    def loop():
        while True:
            with open(log_path, "a") as f:
                f.write(f"Tick: {time.ctime()}\n")
            time.sleep(60)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
