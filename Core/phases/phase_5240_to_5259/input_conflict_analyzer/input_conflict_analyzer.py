# input_conflict_analyzer.py
class InputConflictAnalyzer:
    def find_conflict(self, agent_outputs):
        seen = {}
        for agent, response in agent_outputs.items():
            if response in seen.values():
                continue
            for other_agent, other_response in agent_outputs.items():
                if agent != other_agent and response != other_response:
                    return True, agent, other_agent
        return False, None, None
