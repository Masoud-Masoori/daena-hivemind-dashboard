# curiosity_spark.py
import random

class CuriositySpark:
    def __init__(self):
        self.prompts = [
            "Whats another way to think about this?",
            "Is there a hidden assumption here?",
            "Could this connect to something else youve worked on?"
        ]

    def get_prompt(self):
        return random.choice(self.prompts)
