def merge_responses(responses):
    merged = {}
    for res in responses:
        for k, v in res.items():
            merged.setdefault(k, []).append(v)
    return merged
