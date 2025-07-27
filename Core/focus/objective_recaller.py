class ObjectiveRecaller:
    def __init__(self, objective="launch complete autonomy system"):
        self.core_objective = objective

    def recall(self):
        print(f" Core Objective: {self.core_objective}")
        return self.core_objective
