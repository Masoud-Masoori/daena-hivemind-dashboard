def anchor_memory(signal_id, context_snapshot):
    anchor = {"id": signal_id, "snapshot": context_snapshot}
    print(f"Memory anchor created for: {signal_id}")
    return anchor
