def collapse(history):
    if len(history) <= 3:
        return history
    return history[:1] + ["..."] + history[-2:]
