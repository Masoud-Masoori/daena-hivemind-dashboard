import datetime

def echo_ping():
    return {"echo": True, "timestamp": datetime.datetime.now().isoformat()}

if __name__ == "__main__":
    print("[EchoLink]  Echo Ping: ", echo_ping())
