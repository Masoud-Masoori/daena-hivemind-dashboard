def cleanse_thought(trace):
    terms = ["uh", "maybe", "i think", "kind of"]
    for term in terms:
        trace = trace.replace(term, "")
    return trace.strip()
