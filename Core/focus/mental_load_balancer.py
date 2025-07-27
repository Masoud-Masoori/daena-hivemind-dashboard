class MentalLoadBalancer:
    def __init__(self):
        self.load = []

    def add_task(self, task):
        self.load.append(task)
        print(f" Added to cognitive queue: {task}")

    def balance_load(self):
        if self.load:
            focused = self.load.pop(0)
            print(f" Now focusing on: {focused}")
            return focused
        return " All tasks balanced."
