# fault_injector.py
import random
import logging

class FaultInjector:
    def __init__(self, target_modules):
        self.targets = target_modules

    def inject(self):
        faulty = random.choice(self.targets)
        logging.warning(f"Simulated failure in module: {faulty}")
        return f"Injected fault in {faulty}"
