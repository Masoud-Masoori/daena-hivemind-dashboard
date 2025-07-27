from difflib import SequenceMatcher

def semantic_drift_check(original, current):
    ratio = SequenceMatcher(None, original, current).ratio()
    return ratio < 0.6  # Drift if similarity drops below 60%

if __name__ == "__main__":
    print("[DriftCheck] Drifted?", semantic_drift_check("Process user input", "Process emotional speech"))
