# categorical_drift_anchor.py

expected_categories = {}

def set_baseline(agent_id, categories):
    expected_categories[agent_id] = set(categories)

def detect_drift(agent_id, new_categories):
    expected = expected_categories.get(agent_id, set())
    drifted = set(new_categories) - expected
    return list(drifted)
