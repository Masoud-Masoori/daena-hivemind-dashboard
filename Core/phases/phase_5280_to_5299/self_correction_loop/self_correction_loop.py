# self_correction_loop.py
class SelfCorrectionLoop:
    def evaluate_and_correct(self, response, confidence, correct_fn):
        if confidence < 0.7:
            return correct_fn(response)
        return response
