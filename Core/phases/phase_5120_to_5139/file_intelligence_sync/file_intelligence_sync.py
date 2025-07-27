# file_intelligence_sync.py
import os

class FileIntelligenceSync:
    def __init__(self, folder="D:/Ideas/Daena/files/intel"):
        os.makedirs(folder, exist_ok=True)
        self.folder = folder

    def list_files(self):
        return os.listdir(self.folder)

    def analyze(self, filename):
        path = os.path.join(self.folder, filename)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()[:500]  # Preview
        return "File not found"
