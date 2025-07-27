# live_sync.py
import socket
import json

class LiveSync:
    def __init__(self, host='localhost', port=5050):
        self.host = host
        self.port = port

    def broadcast(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            message = json.dumps(data).encode()
            s.sendto(message, (self.host, self.port))
