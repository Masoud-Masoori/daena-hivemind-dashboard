# hive_firewall.py
class HiveFirewall:
    def __init__(self):
        self.blocked_agents = set()

    def block(self, agent_id):
        self.blocked_agents.add(agent_id)
        print(f"[HiveFirewall] Blocked agent: {agent_id}")

    def is_blocked(self, agent_id):
        return agent_id in self.blocked_agents
