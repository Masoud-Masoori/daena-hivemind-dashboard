### File: core/explainers/decision_explainer.py
import json
import datetime

def explain_decision(llm_votes, selected_model, reason):
    timestamp = datetime.datetime.now().isoformat()
    explanation = {
        "timestamp": timestamp,
        "votes": llm_votes,
        "final_decision": selected_model,
        "reasoning": reason
    }
    log_path = "D:/Ideas/Daena/logs/decision_explanations.log"
    with open(log_path, "a") as f:
        f.write(json.dumps(explanation) + "\n")
    return explanation
