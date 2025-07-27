import requests
from Core.telemetry import log_info, log_error

try:
    response = requests.get("http://localhost:8000/api/v1/agents")
    if response.status_code == 200:
        log_info(" /api/v1/agents endpoint reachable.")
    else:
        log_error(f" /api/v1/agents returned status: {response.status_code}")
except Exception as ex:
    log_error(f" Failed to connect to API: {ex}")
