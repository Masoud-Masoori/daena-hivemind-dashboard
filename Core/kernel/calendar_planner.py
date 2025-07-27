import datetime
def map_tasks_to_calendar(tasks):
    base = datetime.datetime.now().replace(hour=9, minute=0)
    schedule = {}
    for i, task in enumerate(tasks):
        slot = base + datetime.timedelta(minutes=i*45)
        schedule[task] = slot.isoformat()
    print("[PLANNER] Mapped tasks to calendar.")
    return schedule
