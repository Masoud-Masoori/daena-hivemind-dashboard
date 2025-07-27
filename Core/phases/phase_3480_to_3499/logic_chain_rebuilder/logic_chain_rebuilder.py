# logic_chain_rebuilder.py

def rebuild_logical_path(convo_steps):
    logic = []
    for step in convo_steps:
        if 'reasoning' in step:
            logic.append(step['reasoning'])
    return logic if logic else ["No logic trace found."]
