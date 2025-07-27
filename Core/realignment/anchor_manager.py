class AnchorManager:
    def __init__(self):
        self.anchors = []

    def add_anchor(self, label, location):
        self.anchors.append({"label": label, "location": location})

    def list_anchors(self):
        return self.anchors
