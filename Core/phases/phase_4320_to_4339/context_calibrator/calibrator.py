# calibrator.py
class ContextCalibrator:
    def __init__(self, context_window=10):
        self.context = []

    def update_context(self, utterance):
        self.context.append(utterance)
        if len(self.context) > 10:
            self.context.pop(0)

    def get_context(self):
        return self.context
