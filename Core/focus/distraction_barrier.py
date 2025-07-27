class DistractionBarrier:
    def __init__(self):
        self.blocked = []

    def add_distraction(self, task):
        self.blocked.append(task)
        print(f" Distraction logged: {task}")

    def list_distractions(self):
        print(" Distractions recorded:")
        for d in self.blocked:
            print(f" - {d}")
