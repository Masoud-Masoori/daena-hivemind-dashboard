def tune_behavior(agent_profile, context):
    if context == "customer_support":
        agent_profile["verbosity"] = "low"
        agent_profile["tone"] = "empathetic"
    elif context == "debugging":
        agent_profile["verbosity"] = "high"
        agent_profile["tone"] = "technical"
    return agent_profile

if __name__ == "__main__":
    profile = {"name": "Helix", "tone": "default", "verbosity": "default"}
    print("[Tune] ", tune_behavior(profile, "customer_support"))
