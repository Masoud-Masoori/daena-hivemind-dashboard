# decision_fork_reconstructor.py

from collections import defaultdict

fork_registry = defaultdict(list)

def log_decision_fork(agent_id, input_query, fork_outputs):
    fork_registry[agent_id].append((input_query, fork_outputs))

def reconstruct_consensus(agent_id):
    # Majority voting or entropy-based selector
    history = fork_registry[agent_id]
    return history[-1] if history else None
