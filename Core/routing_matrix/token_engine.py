def reward_agent(agent_name, task_quality):
    tokens = {"excellent": 100, "good": 50, "ok": 20, "bad": 0}
    return f"[Reward]  {agent_name} earned {tokens.get(task_quality, 0)} tokens."

if __name__ == "__main__":
    print(reward_agent("ShadowSentinel", "good"))
