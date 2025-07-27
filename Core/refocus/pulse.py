import time

class RefocusPulse:
    def __init__(self, interval=300):
        self.interval = interval  # in seconds

    def pulse(self):
        while True:
            time.sleep(self.interval)
            print(" Refocus Pulse Triggered. Stay aligned with mission.")
