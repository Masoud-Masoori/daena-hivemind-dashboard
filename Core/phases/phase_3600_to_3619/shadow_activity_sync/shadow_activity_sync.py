# shadow_activity_sync.py
def mirror_actions(agent_log):
    shadow_log = [f"[shadow] {entry}" for entry in agent_log]
    return shadow_log
