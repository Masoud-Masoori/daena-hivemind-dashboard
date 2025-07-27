# mastermind_kernel.py
class MastermindKernel:
    def __init__(self):
        self.active_agents = {}

    def register_agent(self, name, agent_obj):
        self.active_agents[name] = agent_obj

    def delegate_task(self, task, context):
        best_agent = max(self.active_agents, key=lambda a: self.active_agents[a].evaluate_fit(task))
        return self.active_agents[best_agent].execute(task, context)

    def report_status(self):
        return {name: agent.status() for name, agent in self.active_agents.items()}
