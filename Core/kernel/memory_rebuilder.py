import json
def rebuild_memory():
    lines = open("D:/Ideas/Daena/logs/checkpoints.jsonl").readlines()
    print(f"[MEMORY] Restoring {len(lines)} context states")
    return [json.loads(l) for l in lines[-5:]]  # last 5 states
