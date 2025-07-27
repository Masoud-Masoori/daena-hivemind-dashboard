def normalize_signal(data):
    if not data:
        return []
    mean_val = sum(data) / len(data)
    return [x - mean_val for x in data]
