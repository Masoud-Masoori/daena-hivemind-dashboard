from core.strategy.time_rules import time_aware_policy
from core.cmp.cmp_decision_gate import verify_risk
from core.cmp.a2a import a2a

# In-memory message bus for agent commands
message_bus = []

def register_agent(agent_name):
    a2a.connect("orchestrator", agent_name)
    print(f"[Orchestrator] Registered agent: {agent_name}")

def execute_task(agent, task):
    if not verify_risk(task):
        return "❌ Task rejected by compliance check."
    policy = time_aware_policy()
    message_bus.append({"agent": agent, "task": task, "policy": policy})
    a2a.broadcast("orchestrator", f"Task '{task}' assigned to {agent} using {policy}")
    return f"Agent {agent} will perform '{task}' using {policy}"
