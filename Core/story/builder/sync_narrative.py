def build_narrative(events):
    return " -> ".join(e["summary"] for e in events if "summary" in e)
