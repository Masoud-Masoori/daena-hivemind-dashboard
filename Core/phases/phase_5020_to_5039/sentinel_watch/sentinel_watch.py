# sentinel_watch.py
import time

class SentinelWatch:
    def __init__(self, log_file="D:/Ideas/Daena/logs/events.log"):
        self.log_file = log_file

    def monitor_logs(self):
        while True:
            with open(self.log_file, "r") as f:
                lines = f.readlines()[-10:]
                for line in lines:
                    if "CRITICAL" in line:
                        print("[Sentinel] Detected CRITICAL issue.")
            time.sleep(5)
