class TaskReturnHandler:
    def __init__(self):
        self.paused_task = None

    def pause(self, task):
        self.paused_task = task
        print(f" Paused task: {task}")

    def resume(self):
        if self.paused_task:
            print(f" Resuming task: {self.paused_task}")
            return self.paused_task
        return " No paused task to resume."
