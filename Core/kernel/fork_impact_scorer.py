def score_fork_duration(start, end):
    from datetime import datetime
    delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    minutes = delta.total_seconds() / 60
    score = "high" if minutes > 30 else "low"
    print(f"[FORK SCORE] {minutes:.1f} min  impact: {score}")
    return score
