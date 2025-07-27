from datetime import datetime

def time_aware_policy():
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    qtr = (now.month - 1) // 3 + 1

    if weekday >= 5:
        return "Low activity - hold ops"
    if qtr == 3 and hour > 15:
        return "Focus on freelance hiring"
    return "Normal ops"
