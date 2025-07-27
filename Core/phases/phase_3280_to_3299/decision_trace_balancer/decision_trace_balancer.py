# decision_trace_balancer.py

from statistics import mode

decision_stack = {}

def record_decision(agent_id, decision):
    if agent_id not in decision_stack:
        decision_stack[agent_id] = []
    decision_stack[agent_id].append(decision)

def get_consensus(agent_id):
    if agent_id in decision_stack:
        try:
            return mode(decision_stack[agent_id])
        except:
            return "No consensus"
    return "Unknown"
