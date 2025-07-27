class MetaGovernorSync:
    def __init__(self):
        self.status = {}

    def update_status(self, department, state):
        self.status[department] = state
        print(f" Governor updated: {department}  {state}")

    def get_status(self):
        return self.status
