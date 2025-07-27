# response_guard.py
class ResponseDeviationGuard:
    def __init__(self):
        self.allowed_deviation = 0.15

    def check_response_alignment(self, reference, response):
        import difflib
        seq = difflib.SequenceMatcher(None, reference, response)
        similarity = seq.ratio()
        return similarity >= (1 - self.allowed_deviation)
