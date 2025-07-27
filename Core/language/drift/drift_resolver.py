def resolve_drift(original, current):
    return f"Alert: Drift from '{original}' to '{current}' detected. Verification required."

if __name__ == "__main__":
    print("[Resolver] ", resolve_drift("Fetch financial data", "Fetch emotional history"))
