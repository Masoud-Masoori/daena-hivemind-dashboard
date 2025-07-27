# objective_refocus_kernel.py
class ObjectiveRefocusKernel:
    def __init__(self, main_objective):
        self.main_objective = main_objective

    def is_on_track(self, current_task):
        return current_task in self.main_objective["milestones"]

    def remind(self):
        return f"Reminder: Stay focused on the primary goal: {self.main_objective['description']}"
