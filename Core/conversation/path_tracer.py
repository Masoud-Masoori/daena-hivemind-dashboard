def trace_conversation_path(thread):
    return [turn["user"] + " -> " + turn["ai"] for turn in thread]
