# llm_disagreement_resolver.py

class LLMDisagreementResolver:
    def resolve(self, answers):
        rated = [{"answer": a, "score": self.score(a)} for a in answers]
        rated.sort(key=lambda x: x["score"], reverse=True)
        return rated[0]["answer"]

    def score(self, answer):
        # Dummy heuristic for now
        return answer.count("data") + answer.count("because")  # favors analytical responses
