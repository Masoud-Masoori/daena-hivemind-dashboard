def sort_by_priority(conflicts):
    return sorted(conflicts, key=lambda x: x.get("urgency", 0), reverse=True)
