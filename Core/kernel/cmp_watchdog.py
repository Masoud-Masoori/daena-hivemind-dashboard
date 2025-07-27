import time, json

def cmp_wake_watchdog():
    while True:
        with open("D:/Ideas/Daena/logs/checkpoints.jsonl", "r") as f:
            lines = f.readlines()
            if lines:
                last = json.loads(lines[-1])
                print(f"[CMP Watchdog] Last checkpoint: {last['event']} in {last['department']}")
        time.sleep(120)
