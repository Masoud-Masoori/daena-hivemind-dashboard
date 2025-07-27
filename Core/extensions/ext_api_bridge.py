import requests
def trigger_external_api(endpoint, payload):
    response = requests.post(endpoint, json=payload)
    print(f"[API] Status: {response.status_code}")
