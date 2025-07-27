def cascade_decision(task, agents):
    results = []
    for agent in agents:
        response = f"{agent} confirms {task}"
        results.append(response)
    print("Cascade complete.")
    return results
