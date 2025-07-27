# daena_reflex_loop.py

class DaenaReflexLoop:
    def __init__(self):
        self.last_state = None

    def observe(self, perception):
        self.last_state = perception
        return f"Reflex: Adjusting to '{perception}'"

    def get_last_state(self):
        return self.last_state
