class FallbackCore:
    def __init__(self, default_strategy="resume_main_objective"):
        self.default_strategy = default_strategy

    def fallback(self, reason):
        print(f" Fallback triggered due to: {reason}")
        print(f"Reverting to strategy: {self.default_strategy}")
