# response_timing_smoother.py
import time
import random

class ResponseTimingSmoother:
    def delay_response(self, min_delay=0.3, max_delay=1.0):
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
