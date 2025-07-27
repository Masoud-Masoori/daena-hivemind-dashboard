# thought_layer_anchor.py
class ThoughtLayerAnchor:
    def __init__(self):
        self.anchors = {}

    def set_anchor(self, agent_id, thought_signature):
        self.anchors[agent_id] = thought_signature

    def verify_anchor(self, agent_id, current_signature):
        return self.anchors.get(agent_id) == current_signature
