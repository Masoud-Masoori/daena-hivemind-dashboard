# meta_timeline_binder.py

class MetaTimelineBinder:
    def __init__(self):
        self.timeline = []

    def bind_event(self, phase, description):
        self.timeline.append({"phase": phase, "desc": description})

    def show_timeline(self):
        return self.timeline
