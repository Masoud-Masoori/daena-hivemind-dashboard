from datetime import datetime
def adjust_by_time(task):
    hour = datetime.now().hour
    if hour >= 18:
        return f"[DELAYED] {task} moved to tomorrow."
    return f"[OK] Executing: {task}"
