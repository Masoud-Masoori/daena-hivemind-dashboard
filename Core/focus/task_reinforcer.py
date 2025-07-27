class TaskReinforcer:
    def __init__(self, roadmap_module):
        self.roadmap_module = roadmap_module

    def nudge(self):
        current = self.roadmap_module.status()
        print(f" Stay focused! {current}")
