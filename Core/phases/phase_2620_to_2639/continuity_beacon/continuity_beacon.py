# continuity_beacon.py
from core.phases.phase_2620_to_2639.intention_trace.intention_trace import log_intention
from core.phases.phase_2620_to_2639.priority_drift.priority_drift import check_drift

def beacon(step_id, context, expected_priority, current_priority):
    drifted = check_drift(current_priority, expected_priority)
    log_intention(step_id, {
        "drifted": drifted,
        "recovered": not drifted,
        "context": context
    })
    if drifted:
        print(f"[Beacon] Drift detected. Phase '{step_id}' is out of sync  logging for recovery.")
    else:
        print(f"[Beacon] Phase '{step_id}' aligned with roadmap.")
