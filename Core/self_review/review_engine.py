def introspect_session(conversation):
    if "uncertain" in conversation.lower():
        return "Needs validation"
    if "contradiction" in conversation.lower():
        return "Flag for correction"
    return "Coherent"
