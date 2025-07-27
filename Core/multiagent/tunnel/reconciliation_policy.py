def reconcile_overrides(tracker_log):
    count = {}
    for entry in tracker_log:
        reason = entry["reason"]
        count[reason] = count.get(reason, 0) + 1
    return {k: v for k, v in count.items() if v > 1}
