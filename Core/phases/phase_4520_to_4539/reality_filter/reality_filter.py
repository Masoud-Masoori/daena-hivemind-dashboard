# reality_filter.py
class RealityFilter:
    def __init__(self, known_facts):
        self.known_facts = known_facts

    def validate(self, statement):
        return statement in self.known_facts
