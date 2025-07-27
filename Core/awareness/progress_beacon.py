class ProgressBeacon:
    def __init__(self):
        self.current_milestone = None

    def set_milestone(self, milestone):
        self.current_milestone = milestone
        print(f" Milestone set: {milestone}")

    def get_status(self):
        return f"Currently focused on: {self.current_milestone}"
