# memory_watchdog.py
import psutil
import time

class MemoryWatchdog:
    def __init__(self, threshold_mb=3000):
        self.threshold = threshold_mb

    def monitor(self):
        mem_used = psutil.virtual_memory().used // (1024 * 1024)
        if mem_used > self.threshold:
            return f"WARNING: Memory usage high: {mem_used}MB"
        return "OK"
