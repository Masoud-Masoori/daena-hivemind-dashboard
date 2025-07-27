# self_mirroring.py

def reflect(agent_id, thoughts):
    print(f"[SelfMirror]  Agent {agent_id} reflecting on thoughts...")
    summarized = " | ".join(thoughts[-3:])
    print(f"[SelfMirror] Recent mental trace: {summarized}")
    return summarized
