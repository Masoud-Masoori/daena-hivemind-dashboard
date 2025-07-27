import os
import time
from .log_telemetry import log_event

def log_startup():
    log_event(" Backend boot sequence started.")

def log_websocket_event(event: str):
    log_event(f" WebSocket: {event}")

def log_api_request(endpoint: str, status: int):
    log_event(f" API {endpoint} => {status}")

def log_intrusion_attempt(ip: str):
    log_event(f" Intrusion attempt from IP: {ip}")
