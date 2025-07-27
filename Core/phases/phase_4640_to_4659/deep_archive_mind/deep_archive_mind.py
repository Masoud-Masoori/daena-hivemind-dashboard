# deep_archive_mind.py
import os
import json

class DeepArchiveMind:
    def __init__(self, archive_path="D:/Ideas/Daena/archive/deep_mind"):
        os.makedirs(archive_path, exist_ok=True)
        self.path = archive_path

    def store(self, label, memory_data):
        with open(os.path.join(self.path, f"{label}.json"), "w") as f:
            json.dump(memory_data, f)

    def retrieve(self, label):
        file = os.path.join(self.path, f"{label}.json")
        if os.path.exists(file):
            with open(file, "r") as f:
                return json.load(f)
        return None
