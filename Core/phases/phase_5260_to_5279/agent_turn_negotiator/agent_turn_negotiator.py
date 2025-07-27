# agent_turn_negotiator.py
class AgentTurnNegotiator:
    def choose_next(self, agents_queue):
        if not agents_queue:
            return None
        return agents_queue.pop(0)
