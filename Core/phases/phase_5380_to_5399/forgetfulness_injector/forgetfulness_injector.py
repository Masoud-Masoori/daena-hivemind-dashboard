# forgetfulness_injector.py

import random

class ForgetfulnessInjector:
    def maybe_forget(self, memory_item, forget_chance=0.1):
        if random.random() < forget_chance:
            return None
        return memory_item
