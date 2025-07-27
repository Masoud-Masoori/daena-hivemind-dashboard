# semantic_compass.py
from difflib import SequenceMatcher

class SemanticCompass:
    def realign(self, current_text, known_topics):
        best_match = None
        best_score = 0.0
        for topic in known_topics:
            score = SequenceMatcher(None, current_text, topic).ratio()
            if score > best_score:
                best_score = score
                best_match = topic
        return best_match
