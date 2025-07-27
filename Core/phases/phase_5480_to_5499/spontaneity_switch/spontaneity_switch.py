# spontaneity_switch.py

import random

class SpontaneitySwitch:
    def __init__(self, creativity_level=0.5):
        self.creativity_level = creativity_level

    def flip(self, input_text):
        if random.random() < self.creativity_level:
            return f" {input_text[::-1]}"
        return input_text
