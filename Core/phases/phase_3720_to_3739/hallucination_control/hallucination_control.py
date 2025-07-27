# hallucination_control.py
class HallucinationRegulator:
    def __init__(self, llm_responses):
        self.history = llm_responses

    def detect_and_flag(self):
        flagged = []
        for r in self.history[-5:]:
            if "?" in r and "fact" not in r:
                flagged.append(r)
        return flagged
