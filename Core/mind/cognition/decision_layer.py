def decision_layers(context):
    return {
        "cognitive_score": 0.92,
        "escalation_ready": context == "urgent",
        "ethics_compliant": True
    }

if __name__ == "__main__":
    print("[Decision Layer] ", decision_layers("urgent"))
