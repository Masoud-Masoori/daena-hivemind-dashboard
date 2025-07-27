import requests, os

def send_alert(subject, target="GmailTrigger"):
    if target == "GmailTrigger":
        print(f"[ALERT] Email would be sent: {subject}")

def post_payload(url, payload):
    requests.post(url, json=payload)

def trigger_event(event_type):
    print(f"[TRIGGER] Event: {event_type}")
