# narrative_replay.py
class NarrativeReplay:
    def __init__(self, index):
        self.index = index

    def replay(self):
        return "\n".join([f"[{e['time']}] {e['speaker']}: {e['text']}" for e in self.index])
