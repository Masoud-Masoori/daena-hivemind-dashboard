# session_journal.py
import datetime

class SessionJournal:
    def __init__(self):
        self.entries = []

    def add_entry(self, speaker, message):
        timestamp = datetime.datetime.now().isoformat()
        self.entries.append({"time": timestamp, "speaker": speaker, "message": message})

    def export(self):
        return self.entries
