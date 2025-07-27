# task_continuity.py
class TaskContinuityMesh:
    def __init__(self):
        self.interrupted_tasks = {}

    def save_task(self, agent_id, task):
        self.interrupted_tasks[agent_id] = task

    def resume_task(self, agent_id):
        return self.interrupted_tasks.pop(agent_id, None)
