# rebuttal_negotiation.py
class RebuttalNegotiation:
    def __init__(self):
        self.history = []

    def suggest_alternative(self, user_input, model_response):
        alt = f"Consider another angle to '{user_input}': What if we also explored...?"
        self.history.append((user_input, model_response, alt))
        return alt

    def get_history(self):
        return self.history
