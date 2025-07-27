# truth_surface_projector.py

def project_truth_surface(statement, context_facts):
    confidence = 0.5
    for fact in context_facts:
        if fact in statement:
            confidence += 0.25
    confidence = min(confidence, 1.0)
    print(f"[TruthProjection]  Projected confidence: {confidence:.2f}")
    return confidence
