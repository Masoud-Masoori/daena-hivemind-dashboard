class PostCrisisResumer:
    def __init__(self):
        self.paused_modules = []

    def pause_module(self, module):
        self.paused_modules.append(module)
        print(f" Paused module: {module}")

    def resume_all(self):
        print(" Resuming all previously paused modules.")
        return self.paused_modules
