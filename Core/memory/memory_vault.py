import json, os

class MemoryVault:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def save_snapshot(self, memory):
        with open(self.path, "r+") as f:
            data = json.load(f)
            data.append(memory)
            f.seek(0)
            json.dump(data, f)
        print(" Memory snapshot saved.")

    def latest(self):
        with open(self.path, "r") as f:
            data = json.load(f)
            return data[-1] if data else None
