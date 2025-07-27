# narrative_builder.py
class NarrativeBuilder:
    def __init__(self):
        self.log = []

    def add_event(self, event):
        self.log.append(event)

    def get_summary(self):
        return " -> ".join(self.log)
