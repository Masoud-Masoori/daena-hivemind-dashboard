def weight_response(quality_metrics):
    weight = 0
    if "relevance" in quality_metrics:
        weight += 0.4 * quality_metrics["relevance"]
    if "accuracy" in quality_metrics:
        weight += 0.4 * quality_metrics["accuracy"]
    if "clarity" in quality_metrics:
        weight += 0.2 * quality_metrics["clarity"]
    return round(weight, 2)
