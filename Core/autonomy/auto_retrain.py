import os, json, datetime

def check_retrain_condition():
    with open("D:\\Ideas\\Daena\\logs\\training_feedback.jsonl") as f:
        data = [json.loads(line) for line in f.readlines()]
    poor_scores = [x for x in data if x["score"] < 6]
    if len(poor_scores) > 10:
        with open("D:\\Ideas\\Daena\\core\\autonomy\\retrain_flag.json", "w") as f:
            f.write(json.dumps({"trigger": True, "reason": "Low success score burst"}))

check_retrain_condition()
