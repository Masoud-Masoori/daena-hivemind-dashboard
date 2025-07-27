def evaluate_threads(thread_states):
    active = [t for t in thread_states if "active" in t]
    return f"[ThreadEval]  {len(active)} active agents."

if __name__ == "__main__":
    print(evaluate_threads(["agent_1:active", "agent_2:idle", "agent_3:active"]))
