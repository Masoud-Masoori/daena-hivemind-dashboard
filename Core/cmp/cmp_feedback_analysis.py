def analyze_feedback(task, rating, notes):
    if rating < 3:
        print(f"[REVIEW] Task '{task}' needs improvement: {notes}")
    else:
        print(f"[OK] Task '{task}' rated {rating}/5")
