from core.agent.registry import get_active_agents
from hybrid.hybrid_llm_selector import choose_model
from rules.constitution import check_ethics
from connectors.a2a_protocol import dispatch_task
from memory.secure_recall import log_event
from core.cmp.cmp_decision_gate import verify_risk
from datetime import datetime

def execute_task(input_text):
    model = choose_model(input_text)
    response = model.generate(input_text)

    if not check_ethics(response):
        log_event("orchestrator", {"timestamp": datetime.now(), "action": "rejected", "reason": "ethics"})
        return "❌ Rejected by constitutional check"

    if not verify_risk(response):
        log_event("orchestrator", {"timestamp": datetime.now(), "action": "rejected", "reason": "risk"})
        return "❌ Rejected by risk check"

    agents = get_active_agents()
    for agent in agents:
        dispatch_task(agent, response)
        log_event(agent["name"], {"timestamp": datetime.now(), "action": "task_dispatched", "task": response})

    log_event("orchestrator", {"timestamp": datetime.now(), "action": "task_completed", "agents": len(agents)})
    return f"✅ Task dispatched to {len(agents)} agents."
