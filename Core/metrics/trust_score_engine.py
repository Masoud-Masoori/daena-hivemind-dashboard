def score_agent(agent_logs):
    if not agent_logs:
        return 0
    trustworthy = sum(1 for log in agent_logs if "error" not in log.lower())
    return int((trustworthy / len(agent_logs)) * 100)

if __name__ == "__main__":
    logs = ["Task completed", "Error on module", "Task completed"]
    print(f"[TrustScore] = {score_agent(logs)}%")
