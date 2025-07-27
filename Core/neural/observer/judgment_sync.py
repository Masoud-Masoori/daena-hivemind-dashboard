def share_judgment(agent_a, agent_b, result):
    return f"{agent_a}  {agent_b}: [SYNC] Judgment = {result}"

if __name__ == "__main__":
    print(share_judgment("FinanceBot", "LegalAI", "Hold Position"))
