import os, time, subprocess
from datetime import datetime

def check_alive(process_name):
    try:
        return process_name in subprocess.check_output("tasklist").decode()
    except:
        return False

def log_status(msg):
    with open("D:\\Ideas\\Daena\\logs\\pulse_log.jsonl", "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {msg}\\n")

while True:
    modules = {
        "CMP": "cmp_guardian_adapter.py",
        "Voice": "xtts_playback.py",
        "LLM": "llm_router.py",
        "UI": "npm run dev"
    }
    for name, cmd in modules.items():
        if not check_alive(name):
            log_status(f"{name} not running. Restarting...")
            subprocess.Popen(["python", f"D:\\Ideas\\Daena\\core\\{name.lower()}"])
    time.sleep(30)
