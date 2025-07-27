# sanity_cascade.py

def sanity_check(agent_thoughts):
    warning_keywords = ['destroy', 'override', 'purge', 'betray']
    alerts = [thought for thought in agent_thoughts if any(word in thought.lower() for word in warning_keywords)]
    if alerts:
        print(f"[SanityCascade]  Flagged thoughts: {alerts}")
    return len(alerts) == 0
