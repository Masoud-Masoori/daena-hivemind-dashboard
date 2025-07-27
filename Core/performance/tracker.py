def track_model_performance(metrics):
    if metrics.get("latency") > 1.0:
        return "slow"
    if metrics.get("accuracy") < 0.75:
        return "underperforming"
    return "optimal"
