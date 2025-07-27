# behavior_mutation_filter.py

def detect_behavior_shift(current_behavior, baseline_behavior):
    diffs = [trait for trait in current_behavior if current_behavior[trait] != baseline_behavior.get(trait)]
    return diffs if diffs else None
