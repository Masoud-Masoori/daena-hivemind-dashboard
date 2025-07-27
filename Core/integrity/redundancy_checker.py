def check_redundancy(agents):
    seen = set()
    for agent in agents:
        if agent["id"] in seen:
            print(f" Redundant agent detected: {agent['id']}")
            return True
        seen.add(agent["id"])
    return False
