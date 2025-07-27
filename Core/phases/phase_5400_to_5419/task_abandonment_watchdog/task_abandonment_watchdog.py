# task_abandonment_watchdog.py

import time

class TaskAbandonmentWatchdog:
    def __init__(self):
        self.active_tasks = {}

    def update_task(self, task_id, timestamp=None):
        self.active_tasks[task_id] = timestamp or time.time()

    def check_for_abandonment(self, timeout_seconds=600):
        now = time.time()
        return [task for task, ts in self.active_tasks.items() if now - ts > timeout_seconds]
