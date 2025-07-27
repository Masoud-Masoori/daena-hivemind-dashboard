import json, os

def send_message(from_id, to, msg_type, body):
    msg = {
        "from": from_id,
        "to": to,
        "type": msg_type,
        "body": body
    }
    path = f"D:\\Ideas\\Daena\\agents\\inbox\\{to}.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(msg) + "\\n")

# Example
send_message("Agent-A", "DataOps", "request", "Run trend detection on 2024 invoices")
