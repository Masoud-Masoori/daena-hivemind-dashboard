class IncidentRecorder:
    def __init__(self):
        self.events = []

    def record_event(self, event):
        self.events.append(event)

    def playback(self):
        for event in self.events:
            print(f"[PLAYBACK] {event}")
