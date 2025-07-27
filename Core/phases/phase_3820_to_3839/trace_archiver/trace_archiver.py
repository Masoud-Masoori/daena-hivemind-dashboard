# trace_archiver.py
import json
import time

class ThoughtTraceArchiver:
    def __init__(self, path="D:/Ideas/Daena/storage/thought_traces.json"):
        self.path = path

    def save_trace(self, trace):
        try:
            with open(self.path, "a") as f:
                f.write(json.dumps({"timestamp": time.time(), "trace": trace}) + "\n")
        except Exception as e:
            print("Archiving failed:", e)
