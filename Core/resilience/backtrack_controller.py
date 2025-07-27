class BacktrackController:
    def __init__(self):
        self.path_log = []

    def log_path(self, step):
        self.path_log.append(step)
        print(f" Logged step: {step}")

    def current_focus(self):
        return self.path_log[-1] if self.path_log else " No path logged yet"

    def resume(self):
        print(" Resuming from last logged step...")
        return self.current_focus()
