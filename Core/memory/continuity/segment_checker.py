def check_segments(memory_log):
    if not memory_log or not isinstance(memory_log, list):
        return False
    for segment in memory_log:
        if "timestamp" not in segment or "content" not in segment:
            return False
    return True
