import datetime, json
def audit_checkpoint(event, dept):
    checkpoint = {
        "timestamp": str(datetime.datetime.now()),
        "event": event,
        "department": dept,
        "status": "triaged"
    }
    with open("D:/Ideas/Daena/logs/checkpoints.jsonl", "a") as log:
        log.write(json.dumps(checkpoint) + "\n")
    print(f"[AUTO-TRIAGE]  Daena routed back to project after: {event}")
