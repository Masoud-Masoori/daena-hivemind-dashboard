# agent_rotation.py

AGENT_POOL = ['finance_agent', 'marketing_agent', 'compliance_agent', 'general_agent']
CURRENT_AGENT_INDEX = 0

def rotate_agent():
    global CURRENT_AGENT_INDEX
    CURRENT_AGENT_INDEX = (CURRENT_AGENT_INDEX + 1) % len(AGENT_POOL)
    active_agent = AGENT_POOL[CURRENT_AGENT_INDEX]
    print(f"[Rotation]  Active agent switched to: {active_agent}")
    return active_agent
