class MultiFocusSupervisor:
    def __init__(self):
        self.active_focus_points = {}

    def assign_focus(self, task, agent):
        self.active_focus_points[agent] = task
        print(f" Agent {agent} assigned to: {task}")

    def verify_focus(self, agent, task_check):
        assigned = self.active_focus_points.get(agent)
        return assigned == task_check
