# specialist_agents.py
class SpecialistAgent:
    def __init__(self, name, expertise_domain):
        self.name = name
        self.domain = expertise_domain
        self.skillset = []

    def assign_skill(self, skill):
        self.skillset.append(skill)

    def describe(self):
        return f"{self.name} specializes in {self.domain} with skills: {', '.join(self.skillset)}"
