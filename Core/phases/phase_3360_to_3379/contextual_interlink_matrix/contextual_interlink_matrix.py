# contextual_interlink_matrix.py

link_matrix = {}

def link_context(agent_id, concept_a, concept_b):
    if agent_id not in link_matrix:
        link_matrix[agent_id] = []
    link_matrix[agent_id].append((concept_a, concept_b))

def get_links(agent_id):
    return link_matrix.get(agent_id, [])
