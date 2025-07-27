# stack_drift_corrector.py

known_states = {}

def report_stack(agent_id, stack):
    known_states[agent_id] = stack
    print(f"[STACK REPORT] {agent_id}  {stack}")

def compare_stack(agent_id, current_stack):
    ref = known_states.get(agent_id)
    if ref and ref != current_stack:
        print(f"[DRIFT DETECTED] {agent_id} stack changed!")
        return True
    return False
