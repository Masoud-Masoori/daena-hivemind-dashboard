ANCHORS = {
    "vision": "build decentralized, adaptive AI-led company",
    "core": "ensure alignment between all agents, departments, and goals",
    "priority": "real-world launch and impact"
}

def verify_against_anchors(input_text):
    for key, value in ANCHORS.items():
        if value.lower() in input_text.lower():
            return True
    return False
