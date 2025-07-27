# redundancy_engine.py
from core.phases.phase_2600_to_2619.decision_checker.decision_checker import validate_decision_set

def redundant_decision(primary_fn, backup_fn, override=None):
    primary = primary_fn()
    backup = backup_fn()
    return validate_decision_set(primary, backup, override)
