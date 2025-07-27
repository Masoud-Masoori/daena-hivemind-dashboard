def adjust_feedback(agent_metrics):
    boosted = {k: v * 1.05 for k, v in agent_metrics.items() if isinstance(v, (int, float))}
    print(f"Boosted metrics: {boosted}")
    return boosted
