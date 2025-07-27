import json, uuid, datetime

def propose_initiative(goal, impact):
    file = f"D:\\Ideas\\Daena\\strategy\\initiatives\\{uuid.uuid4()}.json"
    data = {
        "title": goal,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "expected_impact": impact,
        "status": "pending"
    }
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Example
propose_initiative("Build agent for multilingual support", "Reduce support backlog by 40%")
