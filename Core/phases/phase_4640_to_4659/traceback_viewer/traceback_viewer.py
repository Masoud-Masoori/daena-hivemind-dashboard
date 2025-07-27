# traceback_viewer.py
import json

class TracebackViewer:
    def __init__(self, path="D:/Ideas/Daena/audit/memory_log.jsonl"):
        self.path = path

    def display_trace(self, keyword):
        with open(self.path, "r") as f:
            entries = [json.loads(line) for line in f if keyword in line]
        return entries
