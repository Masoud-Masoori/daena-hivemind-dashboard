# decision_anchor.py
anchors = {}

def anchor_decision(id, rationale):
    anchors[id] = rationale

def get_anchor(id):
    return anchors.get(id, "No anchor found")
