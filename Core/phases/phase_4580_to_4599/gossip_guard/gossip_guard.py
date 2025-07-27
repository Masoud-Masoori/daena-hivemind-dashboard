# gossip_guard.py
class GossipGuard:
    def __init__(self, blacklist_terms):
        self.blacklist = blacklist_terms

    def validate_message(self, message):
        return not any(term in message.lower() for term in self.blacklist)
