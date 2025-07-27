def is_misaligned(agent_actions, policy_goals):
    return not all(action in policy_goals for action in agent_actions)
