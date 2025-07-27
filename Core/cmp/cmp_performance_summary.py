def summarize_agent_performance(agent_data):
    for agent, logs in agent_data.items():
        total = sum(x["revenue"] for x in logs)
        print(f"{agent}: Total Revenue = ${total}")
