# meta_crash_logger.py
import traceback
import datetime

class MetaCrashLogger:
    def __init__(self, log_path="D:/Ideas/Daena/logs/crashes.log"):
        self.log_path = log_path

    def log_exception(self, e: Exception):
        with open(self.log_path, "a") as log:
            log.write(f"\n\n[CRASH] {datetime.datetime.now()}:\n")
            log.write(traceback.format_exc())
            print("[CrashLogger] Crash recorded.")
