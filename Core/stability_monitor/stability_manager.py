def check_stability(current_reply, last_reply):
    if current_reply.strip() == last_reply.strip():
        return "stable"
    diff = abs(len(current_reply) - len(last_reply))
    return "unstable" if diff > 50 else "mostly_stable"
