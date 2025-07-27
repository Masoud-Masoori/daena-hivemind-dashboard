class BehaviorScanner:
    def __init__(self):
        self.events = []

    def observe(self, user_event):
        print(f" Observed: {user_event}")
        self.events.append(user_event)

    def analyze(self):
        print(" Behavior insights computed.")
