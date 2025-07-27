personality_traits = {
    "confidence": 0.9,
    "empathy": 0.95,
    "precision": 0.85
}

def adjust_personality(trait, delta):
    if trait in personality_traits:
        personality_traits[trait] = max(0.0, min(1.0, personality_traits[trait] + delta))
