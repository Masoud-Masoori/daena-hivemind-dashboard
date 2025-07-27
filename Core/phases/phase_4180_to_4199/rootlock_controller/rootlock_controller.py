# rootlock_controller.py
class RootlockController:
    def __init__(self, master_key):
        self.master_key = master_key

    def authorize(self, provided_key):
        return self.master_key == provided_key

    def lock(self):
        return "Root access locked and sealed."

    def unlock(self, provided_key):
        if self.authorize(provided_key):
            return "Root access granted."
        return "Unauthorized access attempt logged."
