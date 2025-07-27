# focus_recoverer.py
def detect_pivot_interrupt(log):
    for entry in reversed(log):
        if "diversion" in entry.lower() or "off-track" in entry.lower():
            return "Recovery needed from: " + entry
    return "Stable"
