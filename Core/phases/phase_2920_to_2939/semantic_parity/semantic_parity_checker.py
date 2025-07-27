# semantic_parity_checker.py

from difflib import SequenceMatcher

def check_semantic_parity(response_1, response_2):
    ratio = SequenceMatcher(None, response_1, response_2).ratio()
    print(f"[SemanticParity]  Similarity ratio: {ratio:.2f}")
    return ratio > 0.85
