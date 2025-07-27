# governance_chain.py
chain_of_command = {
    "Agent": "Lead",
    "Lead": "Director",
    "Director": "Founder"
}

def get_supervisor(role):
    return chain_of_command.get(role, "Unknown")
