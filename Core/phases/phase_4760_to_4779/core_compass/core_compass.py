# core_compass.py
class CoreCompass:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.current_phase = None

    def set_phase(self, phase_id):
        self.current_phase = phase_id

    def get_next_phase(self):
        if self.current_phase in self.roadmap:
            return self.roadmap[self.current_phase].get("next")
        return None
