import time
import os
import logging

log_path = "D:/Ideas/Daena/logs/backend.log"
last_size = 0

logging.basicConfig(filename="D:/Ideas/Daena/logs/error_watcher.log", level=logging.INFO)

def watch():
    global last_size
    while True:
        if not os.path.exists(log_path):
            time.sleep(5)
            continue

        with open(log_path, "r") as f:
            f.seek(last_size)
            new_lines = f.readlines()
            last_size = f.tell()

            for line in new_lines:
                if "ERROR" in line or "Exception" in line:
                    logging.info(f"[ERROR DETECTED] {line.strip()}")

        time.sleep(3)

if __name__ == "__main__":
    watch()
