### File: core/recovery/self_healer.py

import subprocess, os, time

CRITICAL_PATHS = {
    "tts": "tts/xtts.py",
    "wake": "core/wake_loop.py",
    "llm_router": "agents/router/llm_router.py"
}

def check_and_restart():
    for label, path in CRITICAL_PATHS.items():
        full = os.path.join("D:/Ideas/Daena", path)
        if not os.path.exists(full):
            print(f"[Recovery]  Missing {label}. Attempting to restore...")
            # Placeholder  could re-download, re-clone or copy from backup
            time.sleep(2)
            print(f"[Recovery]  Restored dummy {label}")

def recovery_loop():
    print("[Recovery]  Daena self-healing started.")
    while True:
        check_and_restart()
        time.sleep(60)
