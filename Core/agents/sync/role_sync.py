def sync_roles(agent_id, central_db):
    if agent_id in central_db:
        return central_db[agent_id]["roles"]
    return []
