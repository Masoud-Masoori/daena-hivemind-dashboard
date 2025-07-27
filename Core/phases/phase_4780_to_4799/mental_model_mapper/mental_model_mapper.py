# mental_model_mapper.py
class MentalModelMapper:
    def __init__(self):
        self.models = {}

    def update_model(self, agent_id, assumptions):
        self.models[agent_id] = assumptions

    def get_model(self, agent_id):
        return self.models.get(agent_id, {})
