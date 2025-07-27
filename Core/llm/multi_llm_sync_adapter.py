def sync_outputs(outputs):
    majority = max(set(outputs), key=outputs.count)
    return f"[SyncAdapter]  Consensus='{majority}'"

if __name__ == "__main__":
    print(sync_outputs(["Reject", "Approve", "Reject", "Reject"]))
