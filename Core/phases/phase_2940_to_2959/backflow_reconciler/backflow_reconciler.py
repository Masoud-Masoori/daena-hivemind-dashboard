# backflow_reconciler.py

history_log = {}

def reconcile(agent_id, current_msg):
    if agent_id not in history_log:
        history_log[agent_id] = []
    prior = history_log[agent_id][-1] if history_log[agent_id] else ""
    history_log[agent_id].append(current_msg)
    if len(history_log[agent_id]) > 10:
        history_log[agent_id].pop(0)
    if prior and prior != current_msg:
        print(f"[BackflowReconciler]  Agent {agent_id} message diverged. Reconciling with previous context.")
    return True
