class MissionCompass:
    def __init__(self, mission_log):
        self.mission_log = mission_log

    def current_heading(self):
        return self.mission_log[-1] if self.mission_log else " No direction set."

    def update_heading(self, new_heading):
        self.mission_log.append(new_heading)
        print(f" Updated heading: {new_heading}")
