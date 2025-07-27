# continuity_assurance.py

def ensure_thread_continuity(convo_history, min_recall=3):
    relevant = convo_history[-min_recall:] if len(convo_history) >= min_recall else convo_history
    print(f"[Continuity]  Ensured {len(relevant)} items recalled for thread continuity.")
    return relevant
