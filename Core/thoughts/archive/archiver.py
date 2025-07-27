import json
from datetime import datetime

def archive_thought(thought, file_path):
    entry = {"timestamp": datetime.now().isoformat(), "thought": thought}
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
