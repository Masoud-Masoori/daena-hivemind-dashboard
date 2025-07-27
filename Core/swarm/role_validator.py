def validate_role(agent):
    if "role" in agent and agent["role"] in ["observer", "leader", "worker"]:
        print(f" Valid role assigned: {agent['role']}")
        return True
    print(" Invalid or missing role")
    return False
