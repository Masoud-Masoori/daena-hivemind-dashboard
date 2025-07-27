class TaskRejoinEngine:
    def __init__(self):
        self.unfinished_tasks = {}

    def save_task(self, agent_id, task):
        self.unfinished_tasks[agent_id] = task

    def rejoin_task(self, agent_id):
        return self.unfinished_tasks.get(agent_id, None)
