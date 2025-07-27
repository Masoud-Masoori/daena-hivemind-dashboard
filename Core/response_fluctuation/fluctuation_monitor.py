from statistics import mean, stdev

def monitor_fluctuations(response_lengths):
    if len(response_lengths) < 2:
        return "insufficient data"
    variation = stdev(response_lengths)
    return "high variance" if variation > mean(response_lengths) * 0.3 else "normal"
