# trust_alignment_scorer.py

def score_trust(decision, validation, human_override=False):
    trust_score = 100
    if not validation:
        trust_score -= 50
    if human_override:
        trust_score -= 25

    trust_score = max(0, trust_score)
    print(f"[TrustScorer]  Trust score computed: {trust_score}")
    return trust_score
