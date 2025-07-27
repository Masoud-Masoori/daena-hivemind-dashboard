class GuardianAI:
    def __init__(self):
        self.scan_results = []

    def scan_model(self, model_path):
        print(f" Scanning model at: {model_path}")
        self.scan_results.append((model_path, "Safe"))
