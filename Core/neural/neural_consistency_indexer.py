def compute_neural_consistency(outputs):
    if not outputs:
        return 0.0
    consensus = max(set(outputs), key=outputs.count)
    consistency = outputs.count(consensus) / len(outputs)
    return round(consistency, 3)
