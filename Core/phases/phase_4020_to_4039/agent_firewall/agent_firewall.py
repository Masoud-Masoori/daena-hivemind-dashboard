# agent_firewall.py
class AgentFirewall:
    def __init__(self, rules=None):
        self.rules = rules if rules else []

    def add_rule(self, rule_func):
        self.rules.append(rule_func)

    def check(self, message):
        for rule in self.rules:
            if not rule(message):
                return False
        return True
