# dialogue_indexer.py
import datetime

class DialogueIndexer:
    def __init__(self):
        self.index = []

    def add_entry(self, speaker, text):
        timestamp = datetime.datetime.now().isoformat()
        self.index.append({"time": timestamp, "speaker": speaker, "text": text})

    def search(self, keyword):
        return [entry for entry in self.index if keyword.lower() in entry["text"].lower()]
