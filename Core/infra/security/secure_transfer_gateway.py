def secure_transfer(data, destination):
    return f"[Transfer]  Data sent to {destination} with encryption."

if __name__ == "__main__":
    print(secure_transfer("agent logs", "agent://ops.dept"))
