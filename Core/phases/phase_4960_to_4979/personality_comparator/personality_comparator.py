# personality_comparator.py
class PersonalityComparator:
    def __init__(self):
        self.traits = {}

    def register_traits(self, agent_name, openness, conscientiousness, extraversion, agreeableness, neuroticism):
        self.traits[agent_name] = {
            "O": openness,
            "C": conscientiousness,
            "E": extraversion,
            "A": agreeableness,
            "N": neuroticism
        }

    def compare(self, agent1, agent2):
        traits1 = self.traits.get(agent1, {})
        traits2 = self.traits.get(agent2, {})
        return {trait: abs(traits1.get(trait, 0) - traits2.get(trait, 0)) for trait in ["O", "C", "E", "A", "N"]}
