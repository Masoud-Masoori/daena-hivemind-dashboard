import datetime

class TaskTrailTracker:
    def __init__(self):
        self.history = []

    def log_task(self, task_name):
        timestamp = datetime.datetime.now().isoformat()
        self.history.append((task_name, timestamp))
        print(f" Task logged: {task_name} at {timestamp}")

    def get_history(self):
        return self.history
