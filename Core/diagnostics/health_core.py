def run_health_check(agent_status):
    required_keys = ["heartbeat", "response_time", "error_rate"]
    for key in required_keys:
        if key not in agent_status:
            return "incomplete"
    if agent_status["error_rate"] > 0.25:
        return "unstable"
    return "stable"
