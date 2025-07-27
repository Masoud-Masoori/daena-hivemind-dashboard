import socket
import time
import logging

logging.basicConfig(filename="D:/Ideas/Daena/logs/connection_status.log", level=logging.INFO)

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0

def monitor():
    while True:
        frontend = check_port("localhost", 3003)
        backend = check_port("localhost", 8000)
        websocket = check_port("localhost", 8000)  # Same as backend if shared

        logging.info(f"[Status] Frontend: {'UP' if frontend else 'DOWN'} | Backend: {'UP' if backend else 'DOWN'} | WebSocket: {'UP' if websocket else 'DOWN'}")
        time.sleep(5)

if __name__ == "__main__":
    monitor()
