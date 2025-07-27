# resumption_planner.py
from core.phases.phase_2640_to_2659.state_freezer.state_freezer import load_last_state
from core.phases.phase_2640_to_2659.offline_resolver.offline_resolver import resolve_pending_tasks

def resume_system():
    state = load_last_state()
    if state:
        print(f"[Resumption] Resuming from state: {state.get('current_phase')}")
    else:
        print("[Resumption] No prior state. Starting fresh.")
    resolve_pending_tasks()
