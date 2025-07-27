# webhook_activator.py

import requests

def trigger_webhook(url, payload):
    try:
        print(f"[Webhook]  Triggering: {url}")
        response = requests.post(url, json=payload)
        print(f"[Webhook]  Status: {response.status_code}")
    except Exception as e:
        print(f"[Webhook]  Failed: {e}")
