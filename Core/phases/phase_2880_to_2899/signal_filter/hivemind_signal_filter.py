# hivemind_signal_filter.py

def filter_noise(agent_responses, confidence_threshold=0.65):
    filtered = [r for r in agent_responses if r['confidence'] >= confidence_threshold]
    print(f"[SignalFilter]  Filtered {len(filtered)} of {len(agent_responses)} responses.")
    return filtered
