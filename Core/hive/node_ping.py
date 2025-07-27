import random

def ping_neighbors(agent_id, mesh):
    responses = {}
    for neighbor in mesh:
        responses[neighbor] = random.choice(["ok", "delayed", "offline"])
    return responses
