# critical_thread_anchor.py
class CriticalThreadAnchor:
    def __init__(self):
        self.anchors = {}

    def lock_thread(self, key, data):
        self.anchors[key] = data

    def get_anchor(self, key):
        return self.anchors.get(key)
