import json, os

ARCHIVE_PATH = "D:/Ideas/Daena/data/thought_traces.json"

def archive_thought(thought: str):
    if not os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, "w") as f: json.dump([], f)
    with open(ARCHIVE_PATH, "r+") as f:
        data = json.load(f)
        data.append({"thought": thought})
        f.seek(0)
        json.dump(data, f)

if __name__ == "__main__":
    archive_thought("Daena detected anomaly in decision fork.")
    print("[TraceArchiver] Thought archived.")
