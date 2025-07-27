# Syncs temporal context between fast and slow agents
def sync_horizon(agent_pool):
    # sort by reaction latency
    sorted_agents = sorted(agent_pool, key=lambda a: a.response_time)
    return sorted_agents
