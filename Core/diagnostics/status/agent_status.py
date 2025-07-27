def validate_agent_ready(agents):
    print(" Validating all agents for readiness...")
    for a in agents:
        print(f" - {a['name']} status: {' Ready' if a['status'] == 'ready' else ' Not Ready'}")
