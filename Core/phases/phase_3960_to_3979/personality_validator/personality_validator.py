# personality_validator.py

class PersonalityValidator:
    def __init__(self, personality_blueprint):
        self.blueprint = personality_blueprint

    def validate(self, agent_profile):
        for trait, expected in self.blueprint.items():
            if agent_profile.get(trait) != expected:
                return f"Mismatch in trait {trait}: expected {expected}, found {agent_profile.get(trait)}"
        return "Agent personality alignment: PASS"
