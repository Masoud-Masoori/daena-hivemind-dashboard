# sync_alert.py
import time

def notify_mismatch(expected, actual):
    if expected != actual:
        print(f"[SyncAlert] Mismatch Detected: Expected='{expected}' but got '{actual}'")
        # Future: trigger dashboard animation or sound
    else:
        print(f"[SyncAlert] Alignment OK")
