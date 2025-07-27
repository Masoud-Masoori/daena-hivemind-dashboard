class TaskPulseWatcher:
    def __init__(self):
        self.task_states = {}

    def update_pulse(self, task, pulse):
        self.task_states[task] = pulse

    def alert_if_flatlined(self):
        return [task for task, pulse in self.task_states.items() if pulse < 0.2]
