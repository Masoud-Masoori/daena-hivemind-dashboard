# realignment_responder.py

def realign(agent_state, policy_reference):
    corrections = {}
    for k in policy_reference:
        if agent_state.get(k) != policy_reference[k]:
            corrections[k] = policy_reference[k]
    return corrections
