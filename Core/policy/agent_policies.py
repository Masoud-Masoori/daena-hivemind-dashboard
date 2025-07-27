AGENT_POLICIES = {
    "safety": "critical",
    "response_delay": "under 1s",
    "autonomy": "approved if non-critical"
}

def get_policy(key):
    return AGENT_POLICIES.get(key, "[Policy] Not found")

if __name__ == "__main__":
    print(get_policy("safety"))
