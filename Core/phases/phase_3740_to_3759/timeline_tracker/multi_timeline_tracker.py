# multi_timeline_tracker.py
class MultiTimelineTracker:
    def __init__(self):
        self.timelines = {}

    def branch(self, session_id, new_state):
        self.timelines[session_id] = new_state

    def retrieve(self, session_id):
        return self.timelines.get(session_id, {})
