def weighted_response(options):
    # Expect options as list of tuples: (response, weight)
    import random
    total = sum(w for _, w in options)
    r = random.uniform(0, total)
    upto = 0
    for response, weight in options:
        if upto + weight >= r:
            return response
        upto += weight
    return options[0][0]
