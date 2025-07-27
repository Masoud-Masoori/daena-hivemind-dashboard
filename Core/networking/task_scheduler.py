def schedule_task(tasks, agent_map):
    assigned = []
    for task in tasks:
        target = min(agent_map, key=agent_map.get)
        assigned.append((task, target))
        agent_map[target] += 1
    return assigned
