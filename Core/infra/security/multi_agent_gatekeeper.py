def verify_access(agent_id, clearance_level):
    allowed = clearance_level >= 7
    return f"[Gatekeeper] {agent_id} => {'GRANTED' if allowed else 'DENIED'}"

if __name__ == "__main__":
    print(verify_access("agentX", 8))
