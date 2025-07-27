# llm/switcher/llm_router.py
import random
from daena_config import ACTIVE_LLMS

class LLMRouter:
    def __init__(self):
        self.llms = ACTIVE_LLMS

    def choose_model(self, prompt):
        # Placeholder scoring logic (can be replaced with real usage metrics)
        scores = {name: random.random() for name in self.llms}
        return max(scores, key=scores.get)
