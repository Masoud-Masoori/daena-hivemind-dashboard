ongoing_tasks = {"doc_build": "2025-06-05T13:00:00", "pitch_deck": "2025-06-04T17:00:00"}

def track_agenda():
    from datetime import datetime
    now = datetime.now().isoformat()
    for task, deadline in ongoing_tasks.items():
        if now > deadline:
            print(f"[OVERDUE] {task} missed deadline!")
        else:
            print(f"[ON TRACK] {task} due by {deadline}")
