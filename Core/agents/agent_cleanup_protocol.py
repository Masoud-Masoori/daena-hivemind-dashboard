from datetime import datetime, timedelta

agent_expiry = {
    "demo_agent": "2025-06-04T18:30:00"
}

def cleanup_agents(now):
    expired = [a for a, t in agent_expiry.items() if now > t]
    for agent in expired:
        print(f"[EXPIRE] Shutting down agent: {agent}")
