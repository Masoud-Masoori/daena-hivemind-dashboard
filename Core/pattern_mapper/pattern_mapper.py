def detect_patterns(interactions):
    patterns = {}
    for i in interactions:
        if i in patterns:
            patterns[i] += 1
        else:
            patterns[i] = 1
    return {k: v for k, v in patterns.items() if v > 3}
