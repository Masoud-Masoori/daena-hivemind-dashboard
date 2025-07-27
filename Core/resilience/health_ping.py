def health_ping(status="healthy"):
    return f"[Ping]  Status: {status.upper()}"

if __name__ == "__main__":
    print(health_ping("nominal"))
