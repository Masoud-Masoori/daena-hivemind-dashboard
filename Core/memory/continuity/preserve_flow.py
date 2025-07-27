def preserve_continuity(prev_context, current_input):
    if not prev_context:
        return current_input
    if current_input.startswith(prev_context[-1]):
        return current_input
    return prev_context[-1] + " " + current_input
