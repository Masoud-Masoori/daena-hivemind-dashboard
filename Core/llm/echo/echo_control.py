def suppress_echo(responses):
    seen = set()
    unique = []
    for r in responses:
        if r["response"] not in seen:
            seen.add(r["response"])
            unique.append(r)
    return unique
