def build_fallback_chain(primary, alternatives):
    return [primary] + sorted(alternatives, key=lambda x: x["confidence"], reverse=True)
