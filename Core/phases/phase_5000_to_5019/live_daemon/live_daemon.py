# live_daemon.py
import time
import subprocess

class LiveDaemon:
    def __init__(self):
        self.active = True

    def monitor(self, script_path):
        while self.active:
            try:
                subprocess.run(["python", script_path])
            except Exception as e:
                print(f"[Daemon] Error: {e}")
            time.sleep(10)
