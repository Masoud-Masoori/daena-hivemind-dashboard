# persona_reconstruction.py

def reconstruct_persona(agent_memory_log):
    identity = {"traits": [], "interactions": []}
    for record in agent_memory_log:
        if "trait" in record:
            identity["traits"].append(record["trait"])
        if "interaction" in record:
            identity["interactions"].append(record["interaction"])
    return identity
