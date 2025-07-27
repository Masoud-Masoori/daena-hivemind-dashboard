class SignalOverrideCore:
    def __init__(self):
        self.triggers = {}

    def register_trigger(self, signal_name, action_fn):
        self.triggers[signal_name] = action_fn

    def evaluate(self, signal_name):
        if signal_name in self.triggers:
            print(f"[Override Triggered] for {signal_name}")
            return self.triggers[signal_name]()
        return False
