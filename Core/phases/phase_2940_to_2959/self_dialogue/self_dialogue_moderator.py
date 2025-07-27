# self_dialogue_moderator.py

def moderate_internal_dialogue(agent_thoughts):
    flagged = [t for t in agent_thoughts if 'self-terminate' in t.lower()]
    if flagged:
        print(f"[SelfDialogueModerator]  Flagged unsafe self-thoughts: {flagged}")
        return False
    print(f"[SelfDialogueModerator]  All internal thoughts safe.")
    return True
