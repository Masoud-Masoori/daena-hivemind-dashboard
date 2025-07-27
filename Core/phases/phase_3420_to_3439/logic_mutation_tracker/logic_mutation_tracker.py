# logic_mutation_tracker.py

mutation_log = []

def track_mutation(reasoning_input, reasoning_output):
    mutation_log.append((reasoning_input, reasoning_output))
    if len(mutation_log) > 100:
        mutation_log.pop(0)

def summarize_changes():
    return f"Tracked {len(mutation_log)} mutations"
