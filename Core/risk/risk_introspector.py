def introspect_risk(decision_matrix):
    flagged = []
    for step, score in decision_matrix.items():
        if score > 0.8:
            flagged.append((step, score))
    return flagged
