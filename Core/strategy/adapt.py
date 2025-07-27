def adapt_strategy(history, environment_signals):
    if "block" in environment_signals:
        return "defensive"
    elif "opportunity" in environment_signals:
        return "offensive"
    return "neutral"
