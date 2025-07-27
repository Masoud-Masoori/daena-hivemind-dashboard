def extract_majority(tally):
    return max(tally.items(), key=lambda x: x[1])
