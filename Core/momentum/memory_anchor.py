class MemoryAnchor:
    def __init__(self):
        self.anchor_map = {}

    def set_anchor(self, context_id, phase_name):
        self.anchor_map[context_id] = phase_name

    def get_anchor(self, context_id):
        return self.anchor_map.get(context_id, None)
