import time

def log_phase_entry(phase):
    with open("core/log/phase_log.txt", "a") as f:
        f.write(f"[{time.ctime()}] Entered phase: {phase}\n")
