def cascade_alert(origin, affected_agents):
    print(f" Alert from {origin} cascading to:")
    for agent in affected_agents:
        print(f"   -  {agent}")
