# File: core/redundancy/handler.py
def handle_redundant_agents(agent_outputs):
    seen = set()
    filtered = []
    for entry in agent_outputs:
        content = entry.get('content')
        if content and content not in seen:
            seen.add(content)
            filtered.append(entry)
    return filtered
