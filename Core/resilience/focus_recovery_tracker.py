import json, time

def log_context(current_phase, reason, resumed=False):
    log = {
        "timestamp": time.time(),
        "interrupted_phase": current_phase,
        "interruption_reason": reason,
        "resumed": resumed
    }
    with open("logs/recovery_context.json", "w") as f:
        json.dump(log, f, indent=4)
    print("[SIRT] Logged recovery point.")

def resume_after_fix():
    print("[SIRT] Issue resolved. Resuming previous phase...")

if __name__ == "__main__":
    log_context("Phase_2560", "XTTS model missing")
    # Call resume_after_fix() later after resolution
