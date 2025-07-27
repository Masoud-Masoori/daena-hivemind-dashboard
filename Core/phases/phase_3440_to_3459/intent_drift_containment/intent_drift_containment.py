# intent_drift_containment.py

original_prompts = {}

def register_intent(task_id, user_intent):
    original_prompts[task_id] = user_intent

def is_drifting(task_id, latest_output):
    intent = original_prompts.get(task_id, "")
    return intent not in latest_output
