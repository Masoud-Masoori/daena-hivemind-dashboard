# thought_resurfacer.py

class ThoughtResurfacer:
    def __init__(self):
        self.holding_area = []

    def store_interrupted(self, idea):
        self.holding_area.append(idea)

    def resurface_if_triggered(self, trigger_keyword):
        resurfaced = [idea for idea in self.holding_area if trigger_keyword in idea]
        return resurfaced
