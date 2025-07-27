import os
import json
import datetime

def launch_guardian_daemon():
    print("[Guardian]  Daemon initialized.")
    return {"status": "alive", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == "__main__":
    status = launch_guardian_daemon()
    with open("daemon_status.json", "w") as f:
        json.dump(status, f, indent=2)
