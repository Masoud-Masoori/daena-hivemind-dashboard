# conversation_anchor.py
class ConversationAnchor:
    def __init__(self):
        self.anchors = []

    def set_anchor(self, topic):
        self.anchors.append(topic)

    def retrieve(self):
        return self.anchors[-1] if self.anchors else None

    def list_all(self):
        return self.anchors
