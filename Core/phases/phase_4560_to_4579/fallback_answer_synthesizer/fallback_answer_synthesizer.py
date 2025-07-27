# fallback_answer_synthesizer.py
class FallbackAnswerSynthesizer:
    def synthesize(self, context, backup_knowledge):
        return f"[Fallback Synthesis]\nContext: {context}\nKnown: {backup_knowledge}"
