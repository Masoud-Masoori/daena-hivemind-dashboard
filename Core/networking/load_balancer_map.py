def generate_balancer_map(agent_data):
    return {agent["id"]: agent.get("load", 0) for agent in agent_data}
