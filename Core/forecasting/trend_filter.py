def apply_trend_filter(values):
    smoothed = sum(values) / len(values)
    return f"[TrendFilter]  Smoothed Average: {smoothed:.3f}"

if __name__ == "__main__":
    print(apply_trend_filter([0.4, 0.6, 0.8, 1.0]))
