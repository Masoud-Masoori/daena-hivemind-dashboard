def check_recall_trigger(state, thresholds):
    return state.get("urgency", 0) > thresholds.get("recall", 0.8)
