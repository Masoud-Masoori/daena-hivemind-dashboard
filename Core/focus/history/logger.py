import json
import os

class FocusHistoryLogger:
    def __init__(self, log_path="focus_log.json"):
        self.log_path = os.path.join(os.path.dirname(__file__), "history", log_path)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                json.dump([], f)

    def log(self, item):
        with open(self.log_path, "r+") as f:
            data = json.load(f)
            data.append(item)
            f.seek(0)
            json.dump(data, f, indent=2)
