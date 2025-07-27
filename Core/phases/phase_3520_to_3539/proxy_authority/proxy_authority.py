# proxy_authority.py

class ProxyAuthority:
    def __init__(self):
        self.allowed_proxies = []

    def register_proxy(self, agent_id):
        if agent_id not in self.allowed_proxies:
            self.allowed_proxies.append(agent_id)

    def is_proxy_allowed(self, agent_id):
        return agent_id in self.allowed_proxies
