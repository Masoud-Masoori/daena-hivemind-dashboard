import datetime

def snapshot_sync(agent_id):
    timestamp = datetime.datetime.utcnow().isoformat()
    return f"[Snapshot]  Agent {agent_id} synced @ {timestamp}"

if __name__ == "__main__":
    print(snapshot_sync("R2-decision-core"))
