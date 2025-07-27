# meta_judgment_reconciler.py

def reconcile_judgments(agent_votes):
    from collections import Counter
    consensus = Counter(agent_votes).most_common(1)[0][0]
    return consensus
